import argparse
from src.config_manager import ConfigManager
from src.data_loader import DataLoader
from src.api_client import APIClientFactory
from src.query_engine import QueryEngine
from src.response_generator import ResponseGenerator

def main():
    parser = argparse.ArgumentParser(description='AI-powered Data Analysis System')
    parser.add_argument('--file', '-f', type=str, help='Path to data file (CSV or Excel)')
    args = parser.parse_args()

    # Setup configuration
    config_manager = ConfigManager()
    api_config = config_manager.setup_api_configuration()

    # Initialize components
    api_client = APIClientFactory.create_client(api_config)
    data_loader = DataLoader()
    query_engine = QueryEngine(api_client)
    response_generator = ResponseGenerator()

    # Main interaction loop
    while True:
        if not args.file:
            file_path = input("\nEnter the path to your data file (CSV or Excel), or 'exit' to quit: ")
            if file_path.lower() == 'exit':
                break
        else:
            file_path = args.file

        try:
            # Load data
            df = data_loader.load_file(file_path)
            print("\nData loaded successfully!")
            print("\nDataset Overview:")
            print(f"Rows: {len(df)}")
            print(f"Columns: {', '.join(df.columns)}")

            # Interactive query loop
            while True:
                question = input("\nEnter your question about the data (or 'exit' to load a different file): ")
                if question.lower() == 'exit':
                    break

                # Process query and get response
                response = query_engine.process_query(df, question)
                formatted_response = response_generator.format_response(response)
                print("\nAnalysis:")
                print(formatted_response)

            if args.file:  # If file was provided via command line, exit after processing
                break

        except Exception as e:
            print(f"\nError: {str(e)}")
            if args.file:  # If file was provided via command line, exit on error
                break

if __name__ == "__main__":
    main()