R --no-restore --no-save --slave --args ../output/bn_identical.csv ../output/wrr_identical.csv ../output/reordering_identical.pdf < plot_reordering.R
R --no-restore --no-save --slave --args ../output/bn_similar.csv ../output/wrr_similar.csv ../output/reordering_similar.pdf < plot_reordering.R
R --no-restore --no-save --slave --args ../output/bn_pareto_similar.csv ../output/wrr_pareto_similar.csv ../output/reordering_similar_pareto.pdf < plot_reordering.R

