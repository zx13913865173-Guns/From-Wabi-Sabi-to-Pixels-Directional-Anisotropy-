#!/usr/bin/env Rscript
# ------------------------------------------------------------------
# Statistical analyses for the linen-texture study.
# ------------------------------------------------------------------

suppressPackageStartupMessages({
  library(survival)
  library(emmeans)
  library(multcomp)
  library(afex)
})

dir.create("results", showWarnings = FALSE)

# ------------------------------------------------------------------
# Load data
# ------------------------------------------------------------------
exp1_data <- read.csv("results/exp1_data.csv", stringsAsFactors = TRUE)
exp2_data <- read.csv("results/exp2_data.csv", stringsAsFactors = TRUE)
exp4_data <- read.csv("results/exp4_data.csv", stringsAsFactors = TRUE)
exp5_data <- read.csv("results/exp5_data.csv", stringsAsFactors = TRUE)
surv_data <- read.csv("results/survival_data.csv", stringsAsFactors = TRUE)

# ------------------------------------------------------------------
# Experiment 1: 2 x 2 mixed ANOVA
# ------------------------------------------------------------------
exp1_data$participant <- factor(exp1_data$participant)
exp1_data$illuminance <- factor(exp1_data$illuminance)
exp1_data$background  <- factor(exp1_data$background)

aov_exp1 <- aov_car(
  discomfort ~ background * illuminance + Error(participant / background),
  data = exp1_data
)

sink("results/exp1_anova.txt")
print(summary(aov_exp1))
sink()

# Post-hoc: simple effects
posthoc_exp1 <- emmeans(aov_exp1, ~ background | illuminance)
sink("results/exp1_posthoc.txt")
print(pairs(posthoc_exp1))
sink()

# ------------------------------------------------------------------
# Experiment 1: Kaplan-Meier survival (dark condition only)
# ------------------------------------------------------------------
surv_dark <- subset(surv_data, grepl("dark", group))
fit <- survfit(Surv(time, event) ~ group, data = surv_dark)

sink("results/exp1_survival.txt")
print(fit)
print(survdiff(Surv(time, event) ~ group, data = surv_dark))
sink()

# ------------------------------------------------------------------
# Experiment 2: one-way ANOVA with Dunnett post-hoc (vs. A)
# ------------------------------------------------------------------
aov_exp2 <- aov(discomfort ~ condition, data = exp2_data)
sink("results/exp2_anova.txt")
print(summary(aov_exp2))
sink()

dunnett_exp2 <- glht(aov_exp2, linfct = mcp(condition = "Dunnett"))
sink("results/exp2_dunnett.txt")
print(summary(dunnett_exp2))
sink()

# Tukey HSD (for completeness)
tukey_exp2 <- TukeyHSD(aov_exp2)
sink("results/exp2_tukey.txt")
print(tukey_exp2)
sink()

# ------------------------------------------------------------------
# Experiment 4: one-way ANOVA with Dunnett post-hoc (vs. I)
# ------------------------------------------------------------------
exp4_data$condition <- relevel(exp4_data$condition, ref = "I")
aov_exp4 <- aov(discomfort ~ condition, data = exp4_data)
sink("results/exp4_anova.txt")
print(summary(aov_exp4))
sink()

dunnett_exp4 <- glht(aov_exp4, linfct = mcp(condition = "Dunnett"))
sink("results/exp4_dunnett.txt")
print(summary(dunnett_exp4))
sink()

# ------------------------------------------------------------------
# Experiment 5: one-way ANOVA, Dunnett vs. pure white, segmented regression
# ------------------------------------------------------------------
aov_exp5 <- aov(discomfort ~ condition, data = exp5_data)
sink("results/exp5_anova.txt")
print(summary(aov_exp5))
sink()

# Segmented regression on DI level (excluding pure white and linen)
exp5_di <- subset(exp5_data, !is.na(DI_level))
seg_fit <- lm(discomfort ~ DI_level + I(pmax(DI_level - 0.30, 0)),
              data = exp5_di)
sink("results/exp5_segmented.txt")
print(summary(seg_fit))
sink()

cat("Statistical analyses complete. See results/.\n")
