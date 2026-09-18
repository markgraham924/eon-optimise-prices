import importlib.util,json,unittest
from pathlib import Path
SPEC=importlib.util.spec_from_file_location("export_public",Path(__file__).parents[1]/"scripts"/"export_public.py"); M=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(M)
class ExportTests(unittest.TestCase):
 def test_whitelist_drops_private_fields_and_errors(self):
  source={"days":["2026-09-18"],"siteId":"secret","feeds":{"import":{"last_success":10,"error":"token secret"}},"channels":{"import":[{"start":1,"end":2,"latest":3,"first":4,"low":3,"high":4,"changes":1,"day":"2026-09-18","quality":"forecast","history":[[5,6,"forecast"]],"postcode":"M00"}],"export":[]}}
  out=M.transform(source); blob=json.dumps(out)
  self.assertNotIn("secret",blob); self.assertNotIn("siteId",blob); self.assertNotIn("postcode",blob); self.assertNotIn("error",blob)
  self.assertEqual(out["channels"]["import"][0]["history"],[[5.0,6.0]])
 def test_invalid_rows_are_rejected(self):
  out=M.transform({"channels":{"import":[{"start":"bad"}],"export":[]}}); self.assertEqual(out["channels"]["import"],[])
if __name__=="__main__": unittest.main()

