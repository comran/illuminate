all_cpus = ['amd64', 'raspi']

def cpu_select(values):
  for cpu in all_cpus:
    if cpu not in values:
      if 'else' in values:
        values[cpu] = values['else']
      else:
        fail('Need to handle %s CPUs!' % cpu, 'values')
  for key in values:
    if key not in all_cpus and key != 'else':
      fail('Not sure what a %s CPU is!' % key, 'values')
  return select({
    '//tools:cpu_k8': values['amd64'],
    '//tools:cpu_raspi': values['raspi'],
  })
