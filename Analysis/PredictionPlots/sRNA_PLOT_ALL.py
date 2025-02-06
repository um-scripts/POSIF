from srna_plot import read_files, plot

DF, DR = read_files()

# ncRv0140
region = (166910, 167115)
background = [
    (166860, 166910, 'steelblue', r'IGR between \textit{Rv0139} and \textit{Rv0140}'),
    (166910, 167200, 'pink', r"\textit{Rv0140}")
]

plot('ncRv0140', data=DF, region=region, back=background, path='tmp')

# # ncRv3211A
# region = (3587950, 3588064)
# background = [
#     (3587898, 3588120, 'steelblue', r'Sense to \textit{Rv3211}')
# ]
#
# plot('ncRv3211A', data=DF, region=region, back=background, path='FInal_PLOTS')
#
# # ncRv0188A
# region = (219551, 219675)
# background = [
#     (219486, 219700, 'steelblue', r'\textit{Rv0188}')
# ]
#
# plot('ncRv0188A', data=DF, region=region, back=background, path='FInal_PLOTS')
#
# # ncRv0188B
# region = (219705, 219813)
# background = [
#     (219600, 219917, 'steelblue', r'\textit{Rv0188}')
# ]
# plot('ncRv0188B', data=DF, region=region, back=background, path='FInal_PLOTS')
#
# # ncRv0280B
# region = (340746, 340826)
# background = [
#     (340600, 340900, 'steelblue', r'\textit{Rv0280}'),
# ]
# plot('ncRv0280B', data=DF, region=region, back=background, path='FInal_PLOTS')
#
# # ncRv0341
# region = (409939, 410022)
# background = [
#     (409850, 410150, 'steelblue', r'\textit{Rv0341}'),
# ]
# plot('ncRv0341', data=DF, region=region, back=background, path='FInal_PLOTS')

# # ncRv0486uA
#
# region = (574903, 575007)
# background = [
#     (574800, 574903, 'steelblue', r'\textit{Rv0485}'),
#     (574903, 575348, 'pink', r"5'UTR of \textit{Rv0486}"),
#     (575348, 575450, 'palegreen', r'\textit{Rv0486}')
# ]
# TSS = [
#     (574903, 'blue', 'TSS')
# ]
# plot('ncRv0486uA', data=DF, region=region, tss=TSS, back=background, path='FInal_PLOTS')
#
# # ncRv0609u
# region = (704188, 704246)
# background = [
#     (704099, 704241, 'steelblue', r"3'UTR of \textit{Rv0609A}"),
#     (704241, 704300, 'pink', r'IGR between \textit{Rv0609A} and \textit{Rv0610c}')
# ]
# TSS = [(704188, 'blue','TSS')]
# plot('ncRv0609u', data=DF, region=region, tss=TSS, back=background, path='FInal_PLOTS')
# #
# # ncRv1460B
# region = (1646778, 1646874)
# background = [
#     (1646660, 1646950, 'steelblue', r'\textit{Rv1460}'),
# ]
# plot('ncRV1460B', data=DF, region=region, back=background, path='FInal_PLOTS')
#
# # ncRv1847u
# region = (2096760, 2096882)
# background = [
#     (2096700,2096760, 'steelblue', r'IGR between \textit{Rv1846c} and \textit{Rv1847}'),
#     (2096760, 2096877, 'pink', r"5'UTR of \textit{Rv1847}"),
#     (2096877,2097000, 'palegreen', r'\textit{Rv1847}'),
# ]
# TSS = [(2096760, 'blue', 'TSS')]
# plot('ncRv1847u', data=DF, region=region,tss= TSS, back=background, path='FInal_PLOTS')
#
# # ncRv2144
# region = (2404437, 2404548)
# background = [
#     (2404300, 2404521, 'steelblue', r'\textit{Rv2144c}'),
#     ( 2404521, 2404560, 'palegreen', r"5\'UTR of \textit{Rv2144c}")
# ]
# plot('ncRv2144', data=DR, region=region, back=background, path='FInal_PLOTS')
#
# # ncRv2381B
# region = (2668302, 2668380)
# background = [
#     (2668180, 2668500, 'steelblue', r'\textit{Rv2381c}'),
# ]
# plot('ncRv2381B', data=DR, region=region, back=background, path='FInal_PLOTS')
#
# # ncRv2839B
# region = (3146067, 3146189)
# background = [
#     (3146000, 3146300, 'steelblue', r'\textit{Rv2839c}'),
# ]
# plot('ncRv2839B', data=DR, region=region, back=background, path='FInal_PLOTS')
#
# # ncRv3045
# region = (3407034, 3407158)
# background = [
#     (3407000,3407300, 'steelblue', r'\textit{Rv3045}'),
# ]
# TSS = [
#     (3407028, 'blue', 'Internal TSS')
# ]
# plot('ncRv3045', data=DF, region=region, tss=TSS, back=background, path='FInal_PLOTS')
#
# # ncRv3211A
# region = (3587950, 3588064)
# background = [
#     (3587898, 3588120, 'steelblue', r'\textit{Rv3211}')
# ]
# plot('ncRv3211A', data=DF, region=region, back=background, path='FInal_PLOTS')
#
# # ncRv3547i
# region = (3987325, 3987361)
# background = [
#     (3987299, 3987382, 'steelblue', r'IGR between \textit{Rv3547} and \textit{Rv3548c}')
# ]
# plot('ncRv3547i', data=DR, region=region, back=background, path='FInal_PLOTS')
#
# # ncRv3581
# region = (4024053, 4024263)
# background = [
#     (4023868, 4024347, 'steelblue', r'\textit{Rv3581c}')
# ]
# TSS = [
#     (4024263, 'blue', 'Alternative TSS')
# ]
# plot('ncRv3581, data=DR, region=region, back=background, tss=TSS, path='FInal_PLOTS')

# # ncRv366i
# region = (4100656, 4100985)
# background = [
#     (4100510, 4101190, 'steelblue', r'IGR between \textit{Rv3661} and \textit{Rv3662c}')
# ]
# plot('ncRv3661i', data=DF, region=region, back=background, path='FInal_PLOTS')
#
# # ncRv3825F
# region = (4298317, 4298599)
# background = [
#     (4298000, 4298800, 'steelblue', r'\textit{Rv3825c}')
# ]
# plot('ncRv3825F', data=DR, region=region, back=background, path='FInal_PLOTS')
#
#
# # ncRv0510
# region = (602322, 602514)
# background = [
#     (602200, 602600, 'steelblue', r'\textit{Rv0510}')
# ]
# plot('ncRv0510', data=DF, region=region, back=background, path='FInal_PLOTS')
#
# # ncRv3547i
# region = (3987325, 3987361)
# background = [
#     (3987299, 3987382, 'steelblue', r'IGR between \textit{Rv3547} and \textit{Rv3548c}')
# ]
# plot('ncRv3547i', data=DR, region=region, back=background, path='FInal_PLOTS')
#
# # ncRv2381B
# region = (2668302, 2668380)
# background = [
#     (2668200, 2668450, 'steelblue', r'\textit{Rv2381c}')
# ]
# plot('ncRv2381B', data=DR, region=region, back=background, path='FInal_PLOTS')
#
# #
# # ncRv0983B
# region = (1099988, 1100180)
# background = [
#     (1099900, 1100250, 'steelblue', r'\textit{Rv0983}')
# ]
# plot('ncRv0983B', data=DF, region=region, back=background, path='FInal_PLOTS')
#
# # ncRv2711B
# region = (3023882, 3024053)
# background = [
#     (3023800, 3024150, 'steelblue', r'\textit{Rv2711}')
# ]
# plot('ncRv2711B', data=DF, region=region, back=background, path='FInal_PLOTS')
#
# # ncRv2839B
# region = (3146067, 3146189)
# background = [
#     (3146000, 3146250, 'steelblue', r'\textit{Rv2839c}')
# ]
# plot('ncRv2839B', data=DR, region=region, back=background, path='FInal_PLOTS')
#
# # ncRv3616
# region = (4055370, 4056142)
# background = [
#     (4055280, 4056200, 'steelblue', r'\textit{Rv3616c}')
# ]
# plot('ncRv3616', data=DR, region=region, back=background, path='FInal_PLOTS')
#
# # ncRv2226i
# region = (2500381, 2500819)
# background = [
#     (2500373, 2500900, 'steelblue', r'IGR between \textit{Rv2226} and \textit{Rv2227}')
# ]
# plot('ncRv2226i', data=DR, region=region, back=background, path='FInal_PLOTS')
#
# # MTB_sORF_18
# region = (3503301, 3503382)
# background = [
#     (3503277, 3503301, 'palegreen', r'IGR between \textit{Rv3136A} and \textit{Rv3137}'),
#     (3503301, 3503393, 'steelblue', r"5'UTR of \textit{Rv3137}")
# ]
# plot('MTB_sORF_18', data=DF, region=region, back=background, path='FInal_PLOTS')
#
# MTB_sORF_38
region = (3363018, 3363153)
background = [
    (3362986, 3363155, 'steelblue', r"5'UTR of \textit{Rv3003c}"),
    (3363155, 3363255, 'palegreen', r"IGR between \textit{Rv3003c} and \textit{Rv3004}")]

TSS = [(3363155, 'blue', 'TSS')]
plot('MTB_sORF_38', data=DR, region=region, tss=TSS, back=background, path='FInal_PLOTS')


# #ncRv0174
#
# region = (206245, 206344)
# background = [
#     (206180, 206400, 'steelblue', r'\textit{Rv0174}')
# ]
# plot('ncRv0174', data=DF, region=region, back=background, path='FInal_PLOTS')
#
# # MTB_sORF_11
# region = (2048430, 2048611)
# background = [
#     (2048371, 2048700, 'steelblue', r'IGR between \textit{Rv1806} and \textit{Rv1808}')
# ]
# plot('MTB_sORF_11', data=DF, region=region, back=background, path='FInal_PLOTS')
# #
# # MTB_sORF_29
# region = (2421882, 2421991)
# background = [
#     (2421800, 2422000, 'steelblue', r'IGR between \textit{Rv2159c} and \textit{Rv2161c}')
# ]
# plot('MTB_sORF_29', data=DR, region=region, back=background, path='FInal_PLOTS')
#
# # MTB_sORF_MTB_sORF_46
# region = (2551578, 2551636)
# background = [
#     (2551500,2551560,'steelblue',r"5'UTR of \textit{Rv2280}"),
#     (2551560,2553173, 'pink','IGR' ),
#     (2553173,2553180,'palegreen',  r'\textit{Rv2281}')
# ]
# plot('MTB_sORF_46', data=DF, region=region, back=background, path='FInal_PLOTS')
#
# # MTB_sORF_MTB_sORF_44
# region = (4125632, 4125792)
# background = [
#     (4125550,4125850,'steelblue',r"Antisense to \textit{Rv3684}")
# ]
# plot('MTB_sORF_44', data=DR, region=region, back=background, path='FInal_PLOTS')
# #


# # MTB_sORF_13
# region = (2692166, 2692801)
# background = [
#     (2692100, 2692224, 'pink', r"IGR between \textit{Rv2395} and \textit{Rv2395A}"),
#     (2692224, 2692439, 'steelblue', r"\textit{Rv2395A}"),
#     (2692439, 2692551, 'palegreen', r"IGR between \textit{Rv2395A} and \textit{Rv2395B}"),
#     (2692551, 2692715, 'grey', r"\textit{Rv2395B}"),
#     (2692651, 2692799, 'skyblue', r"5'UTR of \textit{Rv2396}"),
#     (2692799, 2693820, 'violet', r"\textit{Rv2396}")]
# TSS = [(2692602, 'blue', 'TSS')]
# plot('MTB_sORF_13_TSS', data=DF, region=region, tss=TSS, back=background, path='FInal_PLOTS')

