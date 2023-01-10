import csv
import os

def mask_to_prefix_length(mask):
  octets = mask.split('.')
  
  if len(octets) != 4:
    raise ValueError('Invalid mask format')
  for octet in octets:
    if not octet.isdigit():
      raise ValueError('Invalid mask format')
  
  octets = [bin(int(octet))[2:].zfill(8) for octet in octets]
  
  mask_bin = ''.join(octets)
  
  prefix_length = mask_bin.index('0')
  
  return prefix_length

print('Files in current directory:')
for i, filename in enumerate(os.listdir(), start=1):
  print(f'{i}. {filename}')

input_number = input('Enter the number of the input CSV file: ')

try:
  input_number = int(input_number)
except ValueError:
  print('Invalid input. Please enter a valid number.')
  exit()

try:
  input_filename = os.listdir()[input_number - 1]
except IndexError:
  print('Invalid input. Please enter a valid number.')
  exit()

with open(input_filename, 'r') as input_file:
  reader = csv.reader(input_file)
  
  row_count = sum(1 for row in reader)
  
  input_file.seek(0)
  
  print(f'Input file has {row_count} rows')
  
  with open('output.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    
    for i, row in enumerate(reader, start=1):
      print(f'Processing row {i}: {row}')
      
      ip_address = row[0]
      mask = row[1]
      
      if '/' in mask:
        print(f'Skipping row {i}: Mask is already in the correct format')
        continue
      
      try:
        prefix_length = mask_to_prefix_length(mask)
      except ValueError as e:
        print(f'Skipping row {i}: {e}')
        continue
      
      combined = f'{ip_address}/{prefix_length}'
      
      writer.writerow([combined])

