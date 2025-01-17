# make_ZToEE_plots.py, a program to draw the L1Studies plots obtained from the histograms extracted from NanoAOD

muselection='#geq 1 tight #mu (p_{{T}} > 25 GeV), pass HLT_IsoMu24'

import yaml
import drawplots
import argparse

def main():
    parser = argparse.ArgumentParser(
        description='''Plotter''',
        usage='use "%(prog)s --help" for more information',
        formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument("-d", "--dir", dest="dir", help="The directory to read the inputs files from and draw the plots to", type=str, default='./')
    parser.add_argument("-c", "--config", dest="config", help="The YAML config to read from", type=str, default='../config_cards/full_PhotonJet.yaml')
    parser.add_argument("-l", "--lumi", dest="lumi", help="The integrated luminosity to display in the top right corner of the plot", type=str, default='')
    parser.add_argument("--plot_nvtx", dest="plot_nvtx", help="Whether or not to draw the plots in bins of nvtx. Default: False", type=bool, default=False)

    args = parser.parse_args()
    config = yaml.safe_load(open(args.config, 'r'))

    input_file = args.dir + "/all_PhotonJet.root"
    if args.lumi != '':
        toplabel="#sqrt{s} = 13.6 TeV, L_{int} = " + args.lumi #+ " fb^{-1}"
    else:
        toplabel="#sqrt{s} = 13.6 TeV"

    # NVTX distribution:
#    drawplots.makedist(
#            inputFiles_list = [input_file],
#            saveplot = True,
#            h1d = ['h_nvtx'],
#            xtitle = 'N_{vtx}',
#            ytitle = 'Events',
#            top_label = toplabel,
#            plotname = 'L1Mu_nvtx',
#            dirname = args.dir + '/plotsL1Run3',
#            )

    for r in config['Regions']:
        region = config['Regions'][r]
        eta_range = "eta{}to{}".format(region[0], region[1]).replace(".","p")
        eta_label = '{{{} #leq | #eta^{{e}}(reco)| < {}}}'.format(region[0], region[1])

        if config['Efficiency']:

            # Efficiency vs Run Number
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + '/plotsL1Run3',
                den = ['h_PlateauEffVsRunNb_Denominator_Jet_plots_{}'.format(eta_range)],
                num = ['h_PlateauEffVsRunNb_Numerator_Jet_plots_{}'.format(eta_range)],
                xtitle = 'run number',
                ytitle = 'Efficiency',
                legendlabels = [],
                extralabel = "#splitline{{#geq 1 tight #mu (p_{{T}} > 25 GeV), pass HLT_IsoMu24, p_{{T}}^{{jet}} > 30 GeV}}{}".format(eta_label),
                top_label = toplabel,
                plotname = "L1Jet_FromEGamma_EffVsRunNb_{}".format(r),
                )

        if config['TurnOns']:
            
            # Efficiency vs pT
            # all eta ranges and all qualities
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + '/plotsL1Run3',
                den = ['h_Jet_plots_{}'.format(eta_range)],
                num = ['h_Jet_plots_{}_l1thrgeq{}'.format(eta_range, thr).replace(".", "p") for thr in  config['Thresholds']],
                xtitle = 'p_{T}^{jet}(reco) (GeV)',
                ytitle = 'Efficiency',
                legendlabels = ['p_{{T}}^{{L1 jet}} #geq {} GeV'.format(thr) for thr in config['Thresholds']],
                #axisranges = [0, 500],
                extralabel = "#splitline{{#geq 1 tight #mu (p_{{T}} > 25 GeV), pass HLT_IsoMu24, p_{{T}}^{{jet}} > 30 GeV}}{}".format(eta_label), 
                setlogx = True,
                top_label = toplabel,
                plotname = 'L1Jet_FromEGamma_TurnOn_{}'.format(r) ,
                )

            # same thing, zoom on the 0 - 50 GeV region in pT
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + '/plotsL1Run3',
                den = ['h_Jet_plots_{}'.format(eta_range)],
                num = ['h_Jet_plots_{}_l1thrgeq{}'.format(eta_range, thr).replace(".", "p") for thr in  config['Thresholds']],
                xtitle = 'p_{T}^{jet}(reco) (GeV)',
                ytitle = 'Efficiency',
                legendlabels = ['p_{{T}}^{{L1 jet}} #geq {} GeV'.format(thr) for thr in config['Thresholds']],
                axisranges = [0, 300],
                extralabel = "#splitline{{#geq 1 tight #mu (p_{{T}} > 25 GeV), pass HLT_IsoMu24, p_{{T}}^{{jet}} > 30 GeV}}{}".format(eta_label), 
                #setlogx = True,
                top_label = toplabel,
                plotname = 'L1Jet_FromEGamma_TurnOn_{}'.format(r) ,
                )

            # TODO: add nvtx plots

    if config['Efficiency']:
        # Efficiency vs Eta Phi
        drawplots.makeeff(
            inputFiles_list = [input_file],
            saveplot = True,
            dirname = args.dir + '/plotsL1Run3',
            num = ['h_L1Jet100vsEtaPhi_Numerator'],
            den = ['h_L1Jet100vsEtaPhi_EtaRestricted'],
            xtitle = '#eta^{jet}(reco)',
            ytitle = '#phi^{jet}(reco)',
            ztitle = 'L1Jet50 efficiency',
            legendlabels = [''],
            extralabel = '#splitline{#geq 1 tight #mu (p_{T} > 25 GeV), pass HLT_IsoMu24}{p_{T}^{jet} > 30 GeV}',
            top_label = toplabel,
            plotname = 'L1Jet_FromEGamma_EffVsEtaPhi',
            axisranges = [-5, 5, -3.1416, 3.1416, 0, 1.1],
            )

    if config['Prefiring']:

        # Postfiring vs Eta Phi
        drawplots.makeeff(
            inputFiles_list = [input_file],
            saveplot = True,
            dirname = args.dir + '/plotsL1Run3',
            num = ['L1Jet100to150_bxplus1_etaphi'],
            den = ['L1Jet100to150_bx0_etaphi'],
            xtitle = '#eta^{jet}(reco)',
            ytitle = '#phi^{jet}(reco)',
            ztitle = 'bx+1 / (bx0 or bx+1)',
            legendlabels = [''],
            extralabel = '#splitline{#geq 1 tight #mu (p_{T} > 25 GeV), pass HLT_IsoMu24}{p_{T}^{jet} > 30 GeV}',
            top_label = toplabel,
            plotname = 'L1Jet_FromEGamma_PostfiringVsEtaPhi',
            axisranges = [-5, 5, -3.1416, 3.1416, 0, 1.1],
            addnumtoden = True,
            )

        # Prefiring vs Eta Phi
        drawplots.makeeff(
            inputFiles_list = [input_file],
            saveplot = True,
            dirname = args.dir + '/plotsL1Run3',
            num = ['L1Jet100to150_bxmin1_etaphi'],
            den = ['L1Jet100to150_bx0_etaphi'],
            xtitle = '#eta^{jet}(reco)',
            ytitle = '#phi^{jet}(reco)',
            ztitle = 'bx-1 / (bx0 or bx-1)',
            legendlabels = [''],
            extralabel = '#splitline{#geq 1 tight #mu (p_{T} > 25 GeV), pass HLT_IsoMu24}{p_{T}^{jet} > 30 GeV}',
            top_label = toplabel,
            plotname = 'L1Jet_FromEGamma_PrefiringVsEtaPhi',
            axisranges = [-5, 5, -3.1416, 3.1416, 0, 1.1],
            addnumtoden = True,
            )

        # Postfiring vs Eta 
        drawplots.makeeff(
            inputFiles_list = [input_file],
            saveplot = True,
            dirname = args.dir + '/plotsL1Run3',
            num = ['L1Jet100to150_bxplus1_eta'],
            den = ['L1Jet100to150_bx0_eta'],
            xtitle = '#eta^{jet}(reco)',
            ytitle = 'bx+1 / (bx0 or bx+1)',
            legendlabels = [''],
            extralabel = '#splitline{#geq 1 tight #mu (p_{T} > 25 GeV), pass HLT_IsoMu24}{p_{T}^{jet} > 30 GeV}',
            top_label = toplabel,
            plotname = 'L1Jet_FromEGamma_PostfiringVsEta',
            axisranges = [-5, 5, 0, 1.1],
            addnumtoden = True,
            )

        # Prefiring vs Eta 
        drawplots.makeeff(
            inputFiles_list = [input_file],
            saveplot = True,
            dirname = args.dir + '/plotsL1Run3',
            num = ['L1Jet100to150_bxmin1_eta'],
            den = ['L1Jet100to150_bx0_eta'],
            xtitle = '#eta^{jet}(reco)',
            ytitle = 'bx-1 / (bx0 or bx-1)',
            legendlabels = [''],
            extralabel = '#splitline{#geq 1 tight #mu (p_{T} > 25 GeV), pass HLT_IsoMu24}{p_{T}^{jet} > 30 GeV}',
            top_label = toplabel,
            plotname = 'L1Jet_FromEGamma_PrefiringVsEta',
            axisranges = [-5, 5, 0, 1.1],
            addnumtoden = True,
            )
       

    regions = config['Regions'].values()
    eta_ranges = ["eta{}to{}".format(region[0], region[1]).replace(".","p") for region in regions]
    eta_labels = ['{} #leq | #eta| < {}'.format(region[0], region[1]) for region in regions]

    if config['Response']:
        # Resolution Vs Pt
        drawplots.makeresol(
            inputFiles_list = [input_file],
            saveplot = True,
            dirname = args.dir + '/plotsL1Run3',
            h2d = ['h_ResponseVsPt_Jet_plots_{}'.format(eta_range) for eta_range in eta_ranges],
            xtitle = 'p_{T}^{reco jet} (GeV)',
            ytitle = '(p_{T}^{L1 jet}/p_{T}^{reco jet})',
            #extralabel = '#splitline{Z#rightarrowee}{Non Iso.}',
            legend_pos = 'top',
            legendlabels = eta_labels,
            top_label = toplabel,
            plotname = 'L1Jet_FromEGamma_ResponseVsPt',
            axisranges = [0, 200, 0, 1.6], 
            )

        # Resolution Vs RunNb
        drawplots.makeresol(
            inputFiles_list = [input_file],
            saveplot = True,
            dirname = args.dir + '/plotsL1Run3',
            h2d = ['h_ResponseVsRunNb_Jet_plots_{}'.format(eta_range) for eta_range in eta_ranges],
            xtitle = 'run number',
            ytitle = '(p_{T}^{L1 jet}/p_{T}^{reco jet})',
            #extralabel = '#splitline{Z#rightarrowee}{Non Iso.}',
            legend_pos = 'top',
            legendlabels = eta_labels,
            top_label = toplabel,
            plotname = 'L1Jet_FromEGamma_ResponseVsRunNb',
            axisranges = [355374, 362760, 0, 2],
            )

        # Zoomed version
        drawplots.makeresol(
            inputFiles_list = [input_file],
            saveplot = True,
            dirname = args.dir + '/plotsL1Run3',
            h2d = ['h_ResponseVsRunNb_Jet_plots_{}'.format(eta_range) for eta_range in eta_ranges],
            xtitle = 'run number',
            ytitle = '(p_{T}^{L1 jet}/p_{T}^{reco jet})',
            #extralabel = '#splitline{Z#rightarrowee}{Non Iso.}',
            legend_pos = 'top',
            legendlabels = eta_labels,
            top_label = toplabel,
            plotname = 'L1Jet_FromEGamma_ResponseVsRunNb_Zoom',
            axisranges = [355374, 362760, 0.8, 1.1],
            )

    # Pt Balance plots

    drawplots.makeprof(
        inputFiles_list = [input_file],
        saveplot = True,
        dirname = args.dir + '/plotsL1Run3',
        h2d = ['h_L1PtBalanceVsRunNb_{}'.format(eta_range) for eta_range in eta_ranges],
        xtitle = 'run number',
        ytitle = '(p_{T}^{L1 jet}/p_{T}^{reco #gamma})',
        extralabel = "#splitline{$selection_label, PFMET<50 GeV}{p_{T}^{jet} > 30 GeV, #Delta#phi(#gamma, jet) > 2.9}",
        legendlabels = eta_labels,
        top_label = toplabel,
        axisranges = [320673, 325173, 0, 1.5],
        plotname = 'L1Jet_FromEGamma_PtBalancevsRun',
        )

    drawplots.makeprof(
        inputFiles_list = [input_file],
        saveplot = True,
        dirname = args.dir + '/plotsL1Run3',
        h2d = ['h_L1PtBalanceVsRunNb_singlejet_{}'.format(eta_range) for eta_range in eta_ranges],
        xtitle = 'run number',
        ytitle = '(p_{T}^{L1 jet}/p_{T}^{reco #gamma})',
        extralabel = "#splitline{$selection_label, PFMET<50 GeV}{= 1 clean jet, p_{T}^{jet} > 30 GeV, #Delta#phi(#gamma, jet) > 2.9}",
        legendlabels = eta_labels,
        top_label = toplabel,
        axisranges = [320673, 325173, 0, 1.5],
        plotname = 'L1Jet_FromEGamma_PtBalancevsRun_singlejet',
        )

if __name__ == '__main__':
    main()
