#!/usr/bin/env python3
"""Structural/link checks and deterministic ODI arithmetic. Not behavioral acceptance."""
import importlib.util,json,re,unittest,sys
sys.dont_write_bytecode=True
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
NAMES=['business-model-canvas','customer-development','odi-outcome-research','switch-interview','value-proposition-canvas','pestel-analysis','porters-five-forces','stp-strategy','opportunity-solution-tree','strategy-canvas']
class SkillStructure(unittest.TestCase):
 def test_entrypoints_and_relative_links(self):
  for name in NAMES:
   with self.subTest(skill=name):
    folder=ROOT/'skills'/name;text=(folder/'SKILL.md').read_text()
    self.assertTrue(text.startswith('---\n'));front=text.split('---',2)[1]
    fields=dict(re.findall(r'^([a-z_-]+): (.+)$',front,re.M))
    self.assertEqual(fields['name'],name);self.assertTrue(0<len(fields['description'])<=1024)
    self.assertLess(len(text.splitlines()),500)
    for f in folder.rglob('*.md'):
     for target in re.findall(r'\]\(([^)]+)\)',f.read_text()):
      if target.startswith(('https://','http://','#')):continue
      self.assertTrue((f.parent/target.split('#')[0]).is_file(),str(f)+' -> '+target)
    for required in ['references/methodology.md','references/sources.md','references/examples.md']:
     self.assertTrue((folder/required).is_file())
 def test_scenario_contracts(self):
  for name in NAMES:
   cases=json.loads((ROOT/'skills'/name/'evals/cases.json').read_text())
   self.assertEqual(len(cases),20);self.assertEqual(len({c['id'] for c in cases}),20)
   self.assertGreaterEqual(sum(not c['expected_activation'] for c in cases),4)
   self.assertTrue(any(c['kind']=='natural' for c in cases))
   for c in cases:
    self.assertTrue(all(c.get(k) for k in ['input','expected_actions','output_requirements','accuracy_checks','pass_criterion','dimensions']))
 def test_no_jtbd_copy_or_unrelated_skill(self):
  self.assertEqual({p.name for p in (ROOT/'skills').iterdir() if p.is_dir()},set(NAMES))
class ODIArithmetic(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  spec=importlib.util.spec_from_file_location('odi_score',ROOT/'skills/odi-outcome-research/scripts/score_outcomes.py');cls.module=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.module)
 def row(self,**kw):return dict({'id':'O1','important':80,'importance_n':100,'satisfied':30,'satisfaction_n':100},**kw)
 def test_under_served(self):
  self.assertEqual(self.module.score_outcomes([self.row()],'clamped')[0]['opportunity'],13)
 def test_overserved_variants(self):
  row=self.row(important=30,satisfied=80)
  self.assertEqual(self.module.score_outcomes([row],'clamped')[0]['opportunity'],3)
  self.assertEqual(self.module.score_outcomes([row],'signed')[0]['opportunity'],-2)
 def test_distinct_valid_denominators(self):
  self.assertEqual(self.module.score_outcomes([self.row(satisfied=40,satisfaction_n=80)],'clamped')[0]['opportunity'],11)
 def test_invalid_counts_and_missing_data(self):
  for kwargs in [{'importance_n':0},{'importance_n':-1},{'important':101},{'satisfied':-1},{'important':True},{'important':1.5},{'satisfaction_n':None}]:
   with self.subTest(kwargs=kwargs),self.assertRaises(ValueError):self.module.score_outcomes([self.row(**kwargs)],'clamped')
 def test_duplicate_ids_and_variant(self):
  with self.assertRaises(ValueError):self.module.score_outcomes([self.row(),self.row()],'clamped')
  with self.assertRaises(ValueError):self.module.score_outcomes([self.row()],'unknown')
 def test_unknown_research_design(self):
  self.assertFalse(self.module.score_outcomes([self.row()],'clamped')[0]['research_design_validated'])
if __name__=='__main__':unittest.main(verbosity=2)
