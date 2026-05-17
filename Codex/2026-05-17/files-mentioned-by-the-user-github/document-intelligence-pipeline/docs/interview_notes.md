# Interview Notes

## 30 Second Explanation

I built a document intelligence pipeline that automates the extraction and validation of invoice data. The free version runs locally with Python and sample documents, but the architecture maps to Azure AI Document Intelligence, Dataverse or SQL, Power BI, and Power Automate in an enterprise environment.

## Problem

Manual document processing is repetitive, slow, and error-prone. Operations teams often copy data from documents into spreadsheets or ERP systems and track exceptions manually.

## My Solution

The pipeline reads incoming documents, extracts important fields, applies validation rules, creates structured outputs, and generates an exception report and dashboard.

## Why This Has Business Impact

- It reduces manual copy-paste work.
- It catches incorrect totals and missing purchase orders.
- It gives managers visibility into approved documents and exceptions.
- It creates structured data that can feed Power BI or ERP systems.

## How I Would Build It In An Enterprise

- Documents arrive through SharePoint or email.
- Power Automate triggers the workflow.
- Azure AI Document Intelligence extracts fields from PDFs or scans.
- Python or Azure Functions applies validation rules.
- Clean records go to Dataverse or SQL.
- Exceptions go to Teams or a review queue.
- Power BI shows volume, value, suppliers, and exception reasons.

## What I Learned

- A useful automation project starts with the business process, not the technology.
- AI extraction is only one part of the system; validation and exception handling make it enterprise-ready.
- A portfolio project becomes stronger when the README explains the business value clearly.

