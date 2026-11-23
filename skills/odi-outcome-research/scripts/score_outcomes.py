#!/usr/bin/env python3
"""Unweighted top-two-box counts -> declared 0–10 scores. No research validation."""
import argparse
import json
import sys

def score_outcomes(rows, variant):
    if variant not in ('clamped', 'signed'):
        raise ValueError('Specify clamped or signed formula variant')
    if not isinstance(rows, list) or not rows:
        raise ValueError('Input must be a nonempty JSON array')
    result, seen = [], set()
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get('id'), str) or not row['id'].strip():
            raise ValueError('Every outcome needs a nonempty string id')
        if row['id'] in seen:
            raise ValueError('Duplicate outcome id: '+row['id'])
        seen.add(row['id'])
        for count, denominator in [('important','importance_n'),('satisfied','satisfaction_n')]:
            if type(row.get(count)) is not int or type(row.get(denominator)) is not int:
                raise ValueError('Unweighted counts and valid denominators must be integers')
            if row[denominator] <= 0 or not 0 <= row[count] <= row[denominator]:
                raise ValueError('Require positive valid n and 0 <= count <= n')
        importance = 10 * row['important'] / row['importance_n']
        satisfaction = 10 * row['satisfied'] / row['satisfaction_n']
        gap = importance - satisfaction
        opportunity = importance + (max(gap, 0) if variant == 'clamped' else gap)
        result.append({**row, 'importance':round(importance,12),
                       'satisfaction':round(satisfaction,12), 'opportunity':round(opportunity,12),
                       'scale':'0-10', 'aggregation':'unweighted top-two-box proportions',
                       'variant':variant, 'research_design_validated':False})
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',help='JSON file with id, important, importance_n, satisfied, satisfaction_n')
    parser.add_argument('--variant',required=True,choices=['clamped','signed'])
    args=parser.parse_args()
    try:
        with open(args.input,encoding='utf-8') as f:rows=json.load(f)
        print(json.dumps(score_outcomes(rows,args.variant),ensure_ascii=False,indent=2))
    except (OSError, ValueError, TypeError) as error:
        parser.error(str(error))

if __name__=='__main__':main()
