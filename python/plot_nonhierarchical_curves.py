import doseresponse as dr
import numpy as np
import numpy.random as npr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import argparse
import sys
import itertools as it

seed = 5
npr.seed(seed)

parser = argparse.ArgumentParser()

parser.add_argument("-a", "--all", action='store_true', help='run hierarchical MCMC on all drugs and channels', default=False)
parser.add_argument("-c", "--num-cores", type=int, help="number of cores to parallelise drug/channel combinations",default=1)

requiredNamed = parser.add_argument_group('required arguments')
requiredNamed.add_argument("--data-file", type=str, help="csv file from which to read in data, in same format as provided crumb_data.csv", required=True)
requiredNamed.add_argument("-m", "--model", type=int, help="For non-hierarchical (put anything for hierarchical):1. fix Hill=1; 2. vary Hill", required=True)

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()

dr.define_model(args.model)
temperature = 1.0
num_params = dr.num_params

# load data from specified data file
dr.setup(args.data_file)

# list drug and channel options, select from command line
# can select more than one of either
drugs_to_run, channels_to_run = dr.list_drug_channel_options(args.all)

num_curves = 750
num_pts = 201


def do_plots(drug_channel):
    drug, channel = drug_channel

    num_expts, experiment_numbers, experiments = dr.load_crumb_data(drug,channel)
    drug,channel,chain_file,images_dir = dr.nonhierarchical_chain_file_and_figs_dir(args.model, drug, channel, temperature)
    
    xmin = 1000
    xmax = -1000
    for expt in experiments:
        a = np.min(expt[:,0])
        b = np.max(expt[:,0])
        if a < xmin:
            xmin = a
        if b > xmax:
            xmax = b
    xmin = int(np.log10(xmin))-1
    xmax = int(np.log10(xmax))+3

    x = np.logspace(xmin,xmax,num_pts)
    
    chain = np.loadtxt(chain_file)
    
    saved_its, h = chain.shape
    
    rand_idx = npr.randint(saved_its, size=num_curves)

    if args.model==1:
        pic50s = chain[rand_idx, 0]
        hills = np.ones(num_curves)
    elif args.model==2:
        pic50s, hills = chain[rand_idx, :2].T

    
    
    fig = plt.figure(figsize=(4,3.2))
    ax = fig.add_subplot(111)
    ax.set_xscale('log')
    ax.grid()
    ax.set_xlim(10**xmin,10**xmax)
    ax.set_ylim(0,100)
    ax.set_xlabel(r'{} concentration ($\mu$M)'.format(drug))
    ax.set_ylabel(r'% {} block'.format(channel))
    #ax.set_title("Inferred dose-response fits")
    for i in xrange(num_curves):
        ax.plot(x, dr.dose_response_model(x,hills[i],dr.pic50_to_ic50(pic50s[i])), color='black', alpha=0.02)
    for expt in experiment_numbers:
        if expt==1:
            ax.plot(experiments[expt][:,0],experiments[expt][:,1],"o",color='orange',ms=10,label='Data',zorder=10)
        else:
            ax.plot(experiments[expt][:,0],experiments[expt][:,1],"o",color='orange',ms=10,zorder=10)
    ax.legend(loc=2,fontsize=12)
    fig.tight_layout()
    print "\n{}\n".format(images_dir)
    fig.savefig(images_dir+"{}_{}_nonh_model_{}_mcmc_prediction_curves.png".format(drug, channel, args.model))
    #fig.savefig(images_dir+"{}_{}_nonh_model_{}_mcmc_prediction_curves.pdf".format(drug, channel, args.model))
    plt.close()
    
    return None

for drug_channel in it.product(drugs_to_run, channels_to_run):
    print drug_channel
    do_plots(drug_channel)


