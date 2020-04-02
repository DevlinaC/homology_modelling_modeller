import sys,os
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

# These are the "Tableau 20" colors as RGB.
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)


def plot_profiles(aln_file, template_profile:list, model_file,model_code):
    e = modeller.environ()
    a = modeller.alignment(e, file=aln_file)

    model = get_profile(model_file, a[model_code])

    # Plot the template and model profiles in the same plot for comparison:
    pylab.figure(1, figsize=(10, 6))
    pylab.xlabel('Alignment position')
    pylab.ylabel('DOPE per-residue score')
    rank = 0
    pylab.plot(model, color=tableau20[rank], linewidth=2, label=model_code)
    for template_code in template_profile:
        rank = rank +1
        templatefile= template_code + ".profile"
        template = get_profile(templatefile, a[template_code])
        pylab.plot(template, color=tableau20[rank], linewidth=2, label=template_code)
    pylab.legend()
    pylab.savefig('dope_profile_best_model.png', dpi=65)
