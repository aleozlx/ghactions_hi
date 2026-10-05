"""Read-only CI evidence experiment. Never authorizes CI or merging."""
import argparse
import json
import subprocess


def assess(run, jobs, expected_head, required_jobs):
    blockers = []
    if run.get('head_sha') != expected_head:
        blockers.append('Run belongs to a different head')
    if run.get('status') != 'completed' or run.get('conclusion') != 'success':
        blockers.append('Run is not successfully completed')
    for name in required_jobs:
        matches = [j for j in jobs if j.get('name') == name]
        if not matches:
            blockers.append('Missing required job: ' + name)
        elif any(j.get('status') != 'completed' or j.get('conclusion') != 'success' for j in matches):
            blockers.append('Required job did not pass: ' + name)
    if not required_jobs:
        blockers.append('Required job coverage is unspecified')
    return {'headMatches': run.get('head_sha') == expected_head,
            'jobRequirementsSatisfied': not blockers,
            'blockers': blockers,
            'testCoverage': 'unknown: inspect collected tests, skips, architecture and scope',
            'mergeAuthorized': False}


def api(endpoint):
    return json.loads(subprocess.check_output(['gh', 'api', '--method', 'GET', endpoint], text=True))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo', default='aleozlx/ghactions_hi')
    p.add_argument('--pr', type=int, required=True)
    p.add_argument('--run', type=int, required=True)
    p.add_argument('--required-job', action='append', default=[])
    args = p.parse_args()
    root = 'repos/' + args.repo
    pr = api(f'{root}/pulls/{args.pr}')
    run = api(f'{root}/actions/runs/{args.run}')
    jobs = []
    page = 1
    while True:
        batch = api(f'{root}/actions/runs/{args.run}/jobs?filter=latest&per_page=100&page={page}')['jobs']
        jobs.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    # Recheck after collecting the run so a moving head cannot silently pass.
    latest = api(f'{root}/pulls/{args.pr}')
    result = assess(run, jobs, latest['head']['sha'], args.required_job)
    if latest['head']['sha'] != pr['head']['sha']:
        result['blockers'].append('PR head changed during inspection')
        result['jobRequirementsSatisfied'] = False
    result.update(repository=args.repo, pr=args.pr, run=args.run,
                  head=latest['head']['sha'], prState=latest['state'])
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
