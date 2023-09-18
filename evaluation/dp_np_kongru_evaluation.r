a1_data <-generate_t_test_data(a1_t_test, group="A1")
a2_data <-generate_t_test_data(a2_t_test, group="A1")
b1_data <-generate_t_test_data(b1_t_test, group="A1")
b2_data <-generate_t_test_data(b2_t_test, group="A1")
c1_data <-generate_t_test_data(c1_t_test, group="A1")

data <- list(
 a1_data$one
)

collect_data_scores(
  data,
  "statistical_data ",
  "training"
)

saveWorkbook(wb, file = "nominal_phrase_results.xlsx",overwrite = TRUE)
