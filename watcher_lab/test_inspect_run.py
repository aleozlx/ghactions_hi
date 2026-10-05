import unittest
from inspect_run import assess


class EvidenceTest(unittest.TestCase):
    def test_green_summary_does_not_cover_skipped_tests(self):
        result = assess({'head_sha':'a','status':'completed','conclusion':'success'},
                        [{'name':'tests','status':'completed','conclusion':'skipped'}], 'a', ['tests'])
        self.assertFalse(result['jobRequirementsSatisfied'])

    def test_other_head_cannot_pass(self):
        result = assess({'head_sha':'old','status':'completed','conclusion':'success'},
                        [{'name':'tests','status':'completed','conclusion':'success'}], 'new', ['tests'])
        self.assertFalse(result['jobRequirementsSatisfied'])

    def test_missing_scope_fails_closed(self):
        self.assertFalse(assess({'head_sha':'a','status':'completed','conclusion':'success'}, [], 'a', [])['jobRequirementsSatisfied'])

    def test_passing_job_is_not_coverage_or_merge_proof(self):
        result = assess({'head_sha':'a','status':'completed','conclusion':'success'},
                        [{'name':'tests','status':'completed','conclusion':'success'}], 'a', ['tests'])
        self.assertTrue(result['jobRequirementsSatisfied'])
        self.assertFalse(result['mergeAuthorized'])
        self.assertTrue(result['testCoverage'].startswith('unknown'))
