# Supply Chain Question Answering Tool

This tool allows users to ask natural language questions related to supply chain operations and receive accurate, contextual answers by synthesizing information from policy documents and supply chain datasets.

## Requirements

*   Python 3.6 or higher
*   pip

## Dependencies

*   fitz (PyMuPDF)
*   pandas

Install the dependencies using the following command:

```
pip install -r requirements.txt
```

## Data Sources

The tool uses two data sources:

1.  **Policy Documents:** PDF files containing internal policies, guidelines, and procedures. These files should be placed in the `Policy Docs/` directory.
2.  **Supply Chain Datasets:** CSV files containing structured supply chain data such as inventory levels, shipments, suppliers, etc. These files should be placed in the `Supply Chain dataset/` directory.

## Usage

1.  Make sure you have the required data sources in the correct directories.
2.  Run the `main.py` script using the following command:

    ```
    python main.py
    ```

3.  The script will prompt you to enter your question. Type your question and press Enter.
4.  The tool will generate an answer based on the available data sources.
5.  To exit the script, type `exit` and press Enter.

## Example Questions

*   What is the company's policy on risk management?
*   What are the key performance indicators (KPIs) for supply chain operations?
*   How does the company ensure data security in its supply chain?

## License

This project is licensed under the MIT License.