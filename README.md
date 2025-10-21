# Python Repositories Chart

This repository automatically updates a chart of the most-starred Python projects on GitHub.

The data is fetched daily using the GitHub REST API and visualized with **Pygal**.

## 🕒 Auto Update

- The workflow `.github/workflows/update_chart.yml` runs every day at 09:00 UTC.
- It generates a new `python_repos.svg` chart and commits it to the repository.

## 🔗 View the Chart

Once GitHub Pages is enabled (Settings → Pages → Deploy from branch `main`),  
you can view the chart here:

👉 **https://<your-username>.github.io/python-repos-stats/python_repos.svg**
