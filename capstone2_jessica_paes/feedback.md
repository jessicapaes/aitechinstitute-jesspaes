# 1. General feedback

Overall, this was a really solid project, and you showed some nice creativity with limited data availability (I know it is hard to find good data for your type of project).

## 1.1. Presentation
- Really nice formatting with clear visuals highlighting the important numbers and background theory.
- It was a little unclear from the slides - and the [business doc](capstone2_jessica_paes/Paes_Jessica_Capstone2_BusinessDoc.md) - who the exact target audience was. It might be good to pick a specific use-case from the outset (e.g. triaging tool for clinicians, personal wellness app, etc.).
- Related to the point above, it would be nice to see a simple graphic to show how this model/app would be used/integrated into a workflow (e.g. `individual takes assessment -> presents to the clinic -> clinician assesses app result -> integrates with other assessments -> makes a decision on how to proceed`).

## 1.2. App
- I ran the app and it ran smoothly, and was easy-to-use, and the results/recommendations were easy to understand. Keeping it simple, and reducing cognitive load is super important for wellness apps (we don't want it to feel like a chore), so I think you handled that aspect nicely!
- The questionnaire section could maybe be reduced even further - for example, a multi-page UI, where the user can scroll through each BFI category one at a time (to reduce information/text overload in a single page). This was probably beyond the scope of the capstone, but could be something to consider during beta-testing phases and get feedback on from real users.

## 1.3. Code
- The notebook itself had really clear documentation and process explanation, which made it super easy to follow!
- The technical implementations of your data processing, analysis, and modelling were pretty much perfect.


# 2.Technical feedback

## 2.1. Label validity / engineering / leakage

I know that there isn't much you can do, given dataset availability, and I'm sure you would have taken a different approach had the data been available. However:
- The risk score is directly calculated from the features themselves, and not tied to a clinical source of validation (i.e. do high risk users actually present with depression and anxiety disorder, in **this specific dataset**).
- The risk score is arbitrarily split into tertiles, which is hard to prove as a meaningful split without a clinical validator (as mentioned above).
- Your risk labels were assigned using cutoff thresholds computed from the **entire dataset**, before the train/test split. This is a less commonly discussed cousin of feature leakage: instead of an input feature carrying test-set information into training, here the target itself was defined using a statistic that included the test set's own values. The practical effect is the same - your test set is no longer a clean read on how the model performs on data it hasn't seen, since the very definition of "correct" for those test rows was partly shaped by those rows. This likely inflates your reported F1/accuracy somewhat.
    - Worth noting that your feature scaling was already done correctly (`scaler.fit_transform(X_train)`, then `.transform(X_test)`). The general practice some data scientists follow - splitting before any EDA or engineering decisions - exists precisely to prevent this class of leakage.
    - This leakage wasn't discussed in detail in the course, since we didn't cover cases where labels are generated from the input feature data itself.

There are some things that need to be addressed, if it is to be deployed for any clinical-adjacent use-cases (including personal wellness tracking, if it is to make the claim of "research-backed").

## 2.2. ML model value
- Given that the Risk score - and therefore the Risk category - is literally defined by a linear transformation of the input features (i.e. `(Neuroticism x 2) - Extraversion - (Conscientiousness x 0.5)`), why do we even need a ML model at all?
- In theory, we could deploy a linear transformation (i.e. the formula), which will take in the feature values, and give a perfect prediction of the risk score, and therefore the risk category.

## 2.3. Dataset calibration to specific demographics
This part kind of relates to everything mentioned above.
- Is this dataset collected from the general population,  those with existing depression & anxiety symptoms, or a mix of both? Depending on this, your label cutoffs may be skewed, and it affects how you can interpret the model's risk categories.
- If the model has never seen very high risk people, it may have a miscalibrated threshold/definition for what risk score is defined as "high risk".
- All of this leads to the question of "once deployed, what is going to define your risk categories?" There are a couple of approaches:
    1. Your training dataset is the ground truth that covers all demographics, and is a true reflection of risk scores observed in the population -> in this scenario, the risk category cutoffs are strictly defined by **risk score value** - based on the tertiles cutoffs observed during training - and you directly apply that same cutoff to new people.
    2. You re-calibrate your risk categories, based on that new person's input -> this means re-applying your tertile cutoffs on `training datset + new input`. This means that who in your dataset is defined as "high risk" will **change**, depending on new input data.

Approach `1.` is preferred here, however, it needs to be backed up with robust data sampling methods. Approach `2.` is far from ideal, but there is a very real scenario where this approach is applied in production (i.e. when the underlying distribution of new data "drifts" from the data that the model was trained on).

## 2.4. Misleading "Risk confidence" scores
- Your final Random Forest model's `.predict_proba()` output is not strictly confidence. It is simply the number of trees in your random forest model that agreed on a predicted class label. In order for this to be a better measure of "confidence", it needs to be "calibrated". I've put a reference to the official scikit-learn docs at the end, which explains it thoroughly. But to summarize:

Raw RF confidence = "how many of the model's internal mini-predictors agreed.". Calibrated confidence = "given past cases where the model said this, how often was it actually correct?"

## 2.5. End-to-end deployment
- To fully deploy an ML project, a few things need to happen:
    1. Python packages and dependencies need to be packaged up into a virtual environment. This allows for your code to run on any new machine, **provided the virtual environment is installed by the user**, with no package version conflicts.
    2. Virtual environments need to further packaged up as a **containerized** application. This allows for the **virtual environment** to be **automatically installed** when you run the application.
    3. The containerized application, can then be **deployed to an end point**. This allows for incoming data to come into the end point (e.g. a storage bucket in AWS), which will then trigger the containerized application to re-train the model, or run predictions on the new data.

To be a full end-to-end Data Scientist, you need to be able to do all of these steps. In some larger organizations, you may have data engineers or MLOps engineers handle steps `2.` and `3.` for you. However, step `1.` is absolutely essential, otherwise your team members will never be able to reproduce and collaborate with your work.

I have worked with many virtual environment management tools, and there is no "one-size-fits-all". However, I would recommend using `uv` (see reference below). Just please never use `pip` - as soon as your project gains a little complexity, it completely fails and can leave you in a really bad spot.

# 3. Some references to supplement the feedback
- We didn't cover it so much in the course (it is more a statistics and research methodology topic), but I feel it is important to understand the [different types of validity](https://www.statsig.com/perspectives/types-of-validity-in-statistics-explained) for your project. Specifically:
    - Whether your risk categories carry "clinical validity" - as I have referred to throughout the feedback - relates to "Measurement Validity", and specifically "Construct validity".
    - Your label leakage issue relates to "External validity"
- [Model drift](https://chalk.ai/blog/data-drift)
- [Confidence calibration](https://scikit-learn.org/stable/modules/calibration.html)
- [Comparing `uv` to other tools](https://medium.com/@dieggo.filipe/uv-the-new-python-package-manager-you-need-to-know-491a147af74c)

