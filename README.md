#### overview

This is a django webapp which:

- Serves out stack-maps of the proper floor for a given callnumber, with the proper aisle-side of the range highlighted.

- Contains code to access (via a cron-job) a google-spreadsheet used by staff for the different libraries and floors. Each row contains the start-callnumber for an aisle-range. The script processes this data into a stand-alone json-file used by the web-app.

- Enables staff to print range-labels.

---

