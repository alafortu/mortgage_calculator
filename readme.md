# Mortgage Calculator

A comprehensive mortgage calculator web application built with Streamlit. It allows users to calculate mortgage payments, visualize the amortization schedule, and understand the breakdown of principal and interest payments over time.

## Features

*   Calculate mortgage payments based on:
    *   Mortgage Amount
    *   Annual Interest Rate
    *   Amortization Period (Years and Months)
    *   Mortgage Term (Years)
    *   Payment Frequency (Monthly, Bi-Weekly, Weekly, Accelerated Bi-Weekly, Accelerated Weekly)
*   Option to simulate the effect of making double payments.
*   Displays key payment details:
    *   Regular payment amount per period
    *   Total number of payments
    *   Total amount paid over the life of the mortgage
*   Interactive visualizations:
    *   **Amortization Table:** Detailed breakdown of each payment into principal and interest, showing the remaining balance.
    *   **Principal vs. Interest Histogram:** Visualizes how the composition of each payment changes over time.
    *   **Balance Over Time Chart:** Shows the decrease in the mortgage balance year by year.

## Installation

1.  **Prerequisites:** Ensure you have Python and pip installed on your system.
2.  **Clone the repository (or download the files):**
    ```bash
    # If using Git:
    # git clone <repository-url>
    # cd mortgage-calculator
    # Otherwise, navigate to the directory containing the files.
    ```
3.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    # source venv/bin/activate
    ```
4.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the application, make sure your virtual environment is activated, navigate to the project directory in your terminal, and run the following command:

```bash
streamlit run mortgage_calculator_app.py
```

This will start the Streamlit server and typically open the application automatically in your default web browser. You can then interact with the sidebar controls to input your mortgage parameters and explore the calculated results and visualizations.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.