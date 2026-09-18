#!/usr/bin/env python3
"""Convert the private collector response to the deliberately small public schema."""
from __future__ import annotations
import argparse, json, math, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ALLOWED_QUALITY={"history","current","forecast"}

def finite_number(value):
    return isinstance(value,(int,float)) and not isinstance(value,bool) and math.isfinite(value)

def clean_row(row):
    required=("start","end","latest","first","low","high")
    if not isinstance(row,dict) or any(not finite_number(row.get(k)) for k in required): return None
    history=[]
    for item in row.get("history",[]):
        if isinstance(item,list) and len(item)>=2 and finite_number(item[0]) and finite_number(item[1]):
            history.append([round(float(item[0]),3),round(float(item[1]),4)])
    return {"start":round(float(row["start"]),3),"end":round(float(row["end"]),3),"day":str(row.get("day",""))[:10],"latest":round(float(row["latest"]),4),"first":round(float(row["first"]),4),"low":round(float(row["low"]),4),"high":round(float(row["high"]),4),"changes":max(0,int(row.get("changes",0))),"quality":row.get("quality") if row.get("quality") in ALLOWED_QUALITY else "forecast","history":history}

def transform(source):
    channels={}
    for name in ("import","export"):
        channels[name]=[c for row in source.get("channels",{}).get(name,[]) if (c:=clean_row(row))]
    latest_success=max([v.get("last_success",0) for v in source.get("feeds",{}).values() if isinstance(v,dict) and finite_number(v.get("last_success",0))] or [0])
    return {"schema_version":1,"published_at":datetime.now(timezone.utc).isoformat(),"observed_at":datetime.fromtimestamp(latest_success,timezone.utc).isoformat() if latest_success else None,"timezone":"Europe/London","region":{"id":"north-west","name":"North West","code":"G","status":"observed"},"tariff":{"name":"E.ON Next Optimise","early_bird_booster":True,"booster_ends":"2027-09-08"},"days":[str(x)[:10] for x in source.get("days",[])],"channels":channels}

def main():
    p=argparse.ArgumentParser(); p.add_argument("--url"); p.add_argument("--input",type=Path); p.add_argument("--output",type=Path,required=True); a=p.parse_args()
    if bool(a.url)==bool(a.input): p.error("provide exactly one of --url or --input")
    if a.url:
        with urllib.request.urlopen(a.url,timeout=20) as r: source=json.load(r)
    else: source=json.loads(a.input.read_text(encoding="utf-8-sig"))
    public=transform(source); a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(public,separators=(",",":"),ensure_ascii=True)+"\n",encoding="utf-8")
    print(f"Published {sum(map(len,public['channels'].values()))} price slots; no customer identifiers or feed errors included.")
if __name__=="__main__": main()

