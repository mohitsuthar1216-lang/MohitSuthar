# Architecture Notes

## Beginner Version

The local project has four simple layers:

1. Intake: read sample documents from `data/samples`.
2. Extraction: pull fields from each document.
3. Validation: check missing fields, dates, totals, and confidence.
4. Reporting: write structured outputs and a dashboard.

This is the same shape as many enterprise automation projects. The tools change, but the thinking stays the same.

## Enterprise Version

```text
SharePoint document library
        |
        v
Power Automate trigger
        |
        v
Azure Function or Logic App
        |
        v
Azure AI Document Intelligence
        |
        v
Validation service
        |
        +--> Dataverse or SQL approved records
        |
        +--> Teams exception notification
        |
        v
Power BI dashboard
```

## Enterprise Design Decisions

- Use Azure AI Document Intelligence when documents are PDFs, scans, or mixed layouts.
- Keep validation separate from extraction because AI output still needs business rules.
- Store every exception with a reason so operations teams can fix source data.
- Never put secrets in the repository. Use Key Vault or environment variables.
- Add audit fields in production: file name, upload time, processed time, model version, and user/team owner.

