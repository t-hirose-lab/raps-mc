"""Compute the frozen 26-region RAPS-MC; Python standard library only.
Inputs must be SUVRs already referenced to cerebellar cortex. No new scaling/fitting.
"""
from pathlib import Path
import csv,json,math,argparse
ROOT=Path(__file__).resolve().parent
def load_parameters(directory=ROOT):
 directory=Path(directory)
 constants=json.loads((directory/'RAPS26_constants.json').read_text())
 with (directory/'RAPS26_coefficients.csv').open(encoding='utf-8-sig',newline='') as f:coeff=list(csv.DictReader(f))
 if len(coeff)!=26 or len({r['region'] for r in coeff})!=26:raise ValueError('Expected 26 unique coefficient rows.')
 for r in coeff:
  for c in ['coefficient','training_mean','training_sd']:r[c]=float(r[c])
  if not all(math.isfinite(r[c]) for c in ['coefficient','training_mean','training_sd']) or r['training_sd']<=0:raise ValueError('Invalid parameters.')
 return constants,coeff
def score_records(records,reference_region,parameter_directory=ROOT):
 if reference_region!='cerebellar_cortex':raise ValueError('Input must already use the cerebellar_cortex reference; this function does not re-reference PET.')
 k,coef=load_parameters(parameter_directory);out=[]
 for i,record in enumerate(records):
  terms=[]
  for r in coef:
   region=r['region']
   if region not in record:raise ValueError(f'Missing region: {region}')
   try:x=float(record[region])
   except (TypeError,ValueError):raise ValueError(f'Non-numeric SUVR at row {i+1}: {region}') from None
   if not math.isfinite(x) or x<=0:raise ValueError(f'SUVR must be finite and positive at row {i+1}: {region}')
   terms.append(r['coefficient']*(x-r['training_mean'])/r['training_sd'])
  raw=k['standardized_intercept']+math.fsum(terms)
  out.append(dict(RAPS_raw=raw,RAPS_z=(raw-k['training_score_mean'])/k['training_score_sd']))
 return out
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--input',required=True);ap.add_argument('--output',required=True)
 ap.add_argument('--reference',required=True,choices=['cerebellar_cortex'])
 ap.add_argument('--parameters',default=str(ROOT));args=ap.parse_args()
 if Path(args.input).resolve()==Path(args.output).resolve():raise ValueError('Input and output must be different files.')
 if Path(args.output).exists():raise FileExistsError('Output exists; choose a new filename.')
 with open(args.input,encoding='utf-8-sig',newline='') as f:
  reader=csv.DictReader(f)
  if reader.fieldnames is None or len(reader.fieldnames)!=len(set(reader.fieldnames)):raise ValueError('Missing or duplicate input column names.')
  records=list(reader)
 if not records:raise ValueError('Input contains no records.')
 scores=score_records(records,args.reference,args.parameters)
 with open(args.output,'x',encoding='utf-8',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=['row_number','RAPS_raw','RAPS_z']);writer.writeheader()
  for i,z in enumerate(scores,1):writer.writerow(dict(row_number=i,**{k:format(v,'.17g') for k,v in z.items()}))
 print(f'Scored {len(scores)} rows with the frozen 26-region model. Scores are not risk probabilities.')
if __name__=='__main__':main()
