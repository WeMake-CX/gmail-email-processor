# Gmail Email Processor

## Overview

The **Gmail Email Processor** is a tool designed to process Gmail mbox files, extract email content, and save the processed emails into text files. It handles decoding MIME words, normalizing text, and ensuring a clean output format.

## Features

- Decodes MIME words in email headers.
- Normalizes text to ensure a maximum of two consecutive line breaks.
- Cleans email bodies to remove unwanted characters.
- Sorts emails by date and writes them to text files based on the sender's domain.

## Setup

### Prerequisites

- Miniconda

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/WEMAKE-CX/gmail-email-processor.git
    cd gmail-email-processor
    ```

2. Run the setup script:

    ```sh
    ./start.sh
    ```

### Usage

1. Place your mbox files in the `source/Gmail` directory.
2. Run the processing script:

    ```sh
    python emailembed.py
    ```

## Code Overview

`emailembed.py`

Handles the processing of mbox files and extraction of email content.

`start.sh`

Sets up the environment using Miniconda and installs required packages.

## Example Output

Processed emails are saved in the `output` directory, with filenames based on the sender's domain.

## License

This project is licensed under the MIT License.
