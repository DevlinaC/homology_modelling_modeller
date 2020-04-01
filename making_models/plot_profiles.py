import pylab
import modeller


def r_enumerate(seq):
    """
    Enumerate a sequence in reverse order
    """
    num = len(seq) - 1
    while num >= 0:
        yield num, seq[num]
        num -= 1


def get_profile(profile_file, seq):
    """
    Read the profile_file into a Python array, and add gaps corresponding to the alignment sequence 'seq'
    """
    # Read all non-comment and non-blank lines from the file:
    f = open(profile_file)
    vals = []
    for line in f:
        if not line.startswith('#') and len(line) > 10:
            spl = line.split()
            vals.append(float(spl[-1]))
    # Insert gaps into the profile corresponding to those in seq:
    for n, res in r_enumerate(seq.residues):
        for gap in range(res.get_leading_gaps()):
            vals.insert(n, None)
    # Add a gap at position '0', so that we effectively count from 1:
    vals.insert(0, None)
    return vals


def plot_profiles(aln_file, template_profile, template_code, model_profile, model_code):
    e = modeller.environ()
    a = modeller.alignment(e, file=aln_file)

    template = get_profile(template_profile, a[template_code])
    model = get_profile(model_profile, a[model_code])

    # Plot the template and model profiles in the same plot for comparison:
    pylab.figure(1, figsize=(10, 6))
    pylab.xlabel('Alignment position')
    pylab.ylabel('DOPE per-residue score')
    pylab.plot(model, color='red', linewidth=2, label=model_code)
    pylab.plot(template, color='green', linewidth=2, label=template_code)
    pylab.legend()
    pylab.savefig('dope_profile_best_model.png', dpi=65)

