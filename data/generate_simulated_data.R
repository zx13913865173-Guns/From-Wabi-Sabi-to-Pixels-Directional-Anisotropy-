# ------------------------------------------------------------------
# Generate simulated data matching the paper's reported means and SDs.
# Replace with real experimental data for actual reproduction.
# ------------------------------------------------------------------

set.seed(20250101)

dir.create("results", showWarnings = FALSE)
dir.create("data",    showWarnings = FALSE)

# ------------------------------------------------------------------
# Experiment 1: 2 (background) x 2 (illuminance) mixed design, N = 60
# ------------------------------------------------------------------
n_per_group <- 30

exp1_data <- data.frame(
  participant = rep(1:(4 * n_per_group), each = 1),
  illuminance = rep(c("dark", "light"), each = 2 * n_per_group),
  background  = rep(rep(c("pure_white", "linen"), each = n_per_group), 2),
  discomfort = c(
    rnorm(n_per_group, 5.83, 1.41),
    rnorm(n_per_group, 3.02, 1.25),
    rnorm(n_per_group, 4.40, 1.52),
    rnorm(n_per_group, 3.52, 1.40)
  ),
  workload = c(
    rnorm(n_per_group, 5.12, 1.63),
    rnorm(n_per_group, 3.45, 1.38),
    rnorm(n_per_group, 4.33, 1.41),
    rnorm(n_per_group, 3.71, 1.44)
  )
)
write.csv(exp1_data, "results/exp1_data.csv", row.names = FALSE)

# ------------------------------------------------------------------
# Experiment 2: 5-level ablation, N = 125 (25 per group)
# ------------------------------------------------------------------
exp2_data <- data.frame(
  condition  = rep(c("A", "B", "C", "D", "E"), each = 25),
  discomfort = c(
    rnorm(25, 5.79, 1.38),
    rnorm(25, 3.11, 1.30),
    rnorm(25, 5.08, 1.55),
    rnorm(25, 4.95, 1.48),
    rnorm(25, 5.38, 1.46)
  ),
  aesthetics = c(
    rnorm(25, 2.22, 0.81),
    rnorm(25, 3.89, 0.78),
    rnorm(25, 2.58, 0.89),
    rnorm(25, 2.65, 0.86),
    rnorm(25, 2.39, 0.88)
  )
)
write.csv(exp2_data, "results/exp2_data.csv", row.names = FALSE)

# ------------------------------------------------------------------
# Experiment 4: 4-level validation, N = 80 (20 per group)
# ------------------------------------------------------------------
exp4_data <- data.frame(
  condition  = rep(c("F", "G", "H", "I"), each = 20),
  discomfort = c(
    rnorm(20, 3.15, 1.31),
    rnorm(20, 3.42, 1.35),
    rnorm(20, 5.61, 1.42),
    rnorm(20, 3.08, 1.28)
  )
)
write.csv(exp4_data, "results/exp4_data.csv", row.names = FALSE)

# ------------------------------------------------------------------
# Experiment 5: 7-level DI validation, N = 210 (30 per group)
# ------------------------------------------------------------------
exp5_data <- data.frame(
  condition  = rep(c("pure_white", "linen", "DI10", "DI20",
                     "DI30", "DI40", "DI50"), each = 30),
  DI_level   = rep(c(NA, 0.38, 0.10, 0.20, 0.30, 0.40, 0.50), each = 30),
  discomfort = c(
    rnorm(30, 5.76, 1.39),
    rnorm(30, 3.10, 1.27),
    rnorm(30, 5.67, 1.40),
    rnorm(30, 5.18, 1.45),
    rnorm(30, 3.46, 1.33),
    rnorm(30, 3.14, 1.29),
    rnorm(30, 3.03, 1.31)
  )
)
write.csv(exp5_data, "results/exp5_data.csv", row.names = FALSE)

# ------------------------------------------------------------------
# Survival data (Experiment 1, < 1 lx)
# Simulated from reported medians: pure white 7.8 min, linen 13.5 min
# ------------------------------------------------------------------
sim_surv <- function(n, median, cap = 20) {
  # Weibull approximation matching the median
  k  <- 1.5
  lam <- median / (log(2) ^ (1 / k))
  t  <- lam * (-log(runif(n))) ^ (1 / k)
  event <- as.integer(t <= cap)
  t <- pmin(t, cap)
  data.frame(time = t, event = event)
}

set.seed(42)
pw_dark    <- sim_surv(30, 7.8)
ln_dark    <- sim_surv(30, 13.5)
surv_data  <- rbind(
  data.frame(pw_dark, group = "pure_white_dark"),
  data.frame(ln_dark, group = "linen_dark")
)
write.csv(surv_data, "results/survival_data.csv", row.names = FALSE)

cat("Simulated data written to results/.\n")
