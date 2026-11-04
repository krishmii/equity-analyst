# Strategy Manager (a checklist in code, not a model)

The Manager is code: agent_team/manager.py. It does not call a model.

1. Check the five parts are present, each as a `## ` heading:
   Overview; Market Positioning and Growth Outlook; Valuation Insights;
   Future Developments and Strategic Recommendations; Investment Recommendation.
2. Check consistency: the Investment Recommendation has exactly one `Recommendation:` line
   (Buy, Hold or Sell) and a `Deciding number:` line.
3. A part that fails goes back to the role that owns it ONE time only. No role runs more than twice.
4. Compile the report. Flags that still fail after the retry are written at the top.
