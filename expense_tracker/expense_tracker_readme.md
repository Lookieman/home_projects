# Expense Tracker

A Python-based automated expense tracking system that processes receipt screenshots using AI, converts foreign currencies, and generates organized Excel reports for personal financial management.

## Overview

This system automates the tedious process of manually tracking expenses from receipts. It uses Claude AI to extract data from receipt images, converts foreign currencies to SGD, and organizes transactions into weekly Excel sheets for easy analysis.

### Key Features

- 🤖 **AI-Powered Receipt Processing**: Uses Claude 3.5 Sonnet to extract merchant names, amounts, dates, and payment methods
- 💱 **Automatic Currency Conversion**: Converts foreign currencies to SGD using real-time exchange rates
- 📊 **Excel Report Generation**: Creates organized weekly sheets with automatic totaling
- 📅 **Custom Date Cycles**: Tracks expenses from 19th of previous month to 12th of current month
- 🔍 **Manual Review System**: Flags uncertain extractions for human verification
- 🔒 **Privacy-Focused**: Processes images locally, only sends receipt data (no personal identifiers)

## Project Structure

```
expense_tracker/
├── scripts/
│   ├── file_manager.py          # File movement and organization
│   ├── receipt_processor.py     # AI-powered receipt analysis
│   ├── excel_manager.py         # Excel report generation
│   ├── currency_converter.py    # Foreign exchange conversion
│   └── main.py                  # Main orchestration script
├── data/
│   ├── Archive/                 # Processed receipt images
│   └── processing_log.json      # Processing history
├── result/
│   └── expense_<month>.xlsx     # Generated monthly reports
├── config/
│   ├── .env                     # API keys and configuration
│   └── categories.json          # Expense categorization rules
├── requirements.txt
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Claude API key from Anthropic
- gdrive folder: `C:\Users\luqma\gdrive\expense_inbox`

### Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/Lookieman/home_projects.git
   cd home_projects/expense_tracker
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create `config/.env`:
   ```env
   CLAUDE_API_KEY=your_claude_api_key_here
   CURRENCY_API_KEY=your_currency_api_key_here  # Optional, free tier available
   ```

4. **Configure paths** in `config/settings.py`:
   ```python
   gdrive_INBOX = "C:/Users/luqma/gdrive/expense_inbox"
   DATA_FOLDER = "C:/home_projects/expense_tracker/data"
   RESULTS_FOLDER = "C:/home_projects/expense_tracker/result"
   ```

## Usage

### Basic Workflow

1. **Take receipt photos** and save to gdrive expense_inbox folder
2. **Run file transfer** (can be automated on startup):
   ```bash
   python scripts/file_manager.py
   ```
3. **Process receipts**:
   ```bash
   python scripts/main.py
   ```
4. **Review results** in generated Excel files

### Expected Input Formats

The system handles various receipt types:
- **Local receipts** (SGD): SINOPEC, restaurants, retail stores
- **Foreign receipts**: Malaysia (RM), other countries
- **Digital payments**: PayNow, PayLah transfers
- **Card transactions**: DBS Credit Card (ending 2920), Trust Credit Card (ending 6536)

### Output Format

Monthly Excel files with structure:
- **Week 1-4 sheets**: Individual weekly transactions
- **Total sheet**: Consolidated summary
- **Review sheet**: Transactions requiring manual verification

## Technical Details

### AI Processing Pipeline

1. **Image Preprocessing**: Resize and optimize for Claude API
2. **Data Extraction**: Structured prompt returns JSON with:
   ```json
   {
     "merchant_name": "SINOPEC Pasir Ris",
     "amount": 43.51,
     "currency": "SGD",
     "date": "2025-06-20",
     "payment_method": "DBS Credit Card 2920",
     "confidence": 0.95
   }
   ```
3. **Currency Conversion**: Real-time rates for foreign transactions
4. **Validation**: Confidence scoring and error flagging

### Privacy & Security

- ✅ No personal identifiers sent to external APIs
- ✅ Receipt images processed locally
- ✅ Only merchant names and amounts shared with Claude
- ✅ No spending pattern analysis stored externally
- ✅ API keys stored in local environment files

### Cost Estimation

- **Claude API**: ~$1 SGD/month (60 receipts)
- **Currency API**: Free tier (1500 requests/month)
- **Total**: Under $2 SGD/month

## Configuration

### Expense Categories

Edit `config/categories.json` to customize categorization:
```json
{
  "food": ["restaurant", "cafe", "mcdonald", "kfc"],
  "transport": ["grab", "taxi", "mrt", "parking"],
  "shopping": ["shopee", "lazada", "amazon"],
  "utilities": ["sp digital", "phone", "internet"]
}
```

### Date Cycle Customization

Modify the tracking period in `scripts/excel_manager.py`:
- Current: 19th of previous month to 12th of current month
- Adjust `CYCLE_START_DAY` and `CYCLE_END_DAY` variables

## Development Roadmap

### Phase 1: Core Functionality ✅
- [x] File management system
- [x] Claude API integration
- [x] Currency conversion
- [x] Excel generation

### Phase 2: Enhancement Features 🔄
- [ ] Automatic categorization
- [ ] Budget tracking and alerts
- [ ] Monthly spending analysis
- [ ] Receipt image archival system

### Phase 3: Advanced Features 📋
- [ ] Mobile app integration
- [ ] Real-time spending notifications
- [ ] Predictive spending analysis
- [ ] Integration with bank APIs

## Troubleshooting

### Common Issues

1. **API Rate Limits**: Claude has generous limits, but heavy usage may require rate limiting
2. **Image Quality**: Poor receipt photos may require manual data entry
3. **Currency Conversion**: Foreign transactions use receipt date for exchange rates
4. **Excel Permissions**: Ensure Excel files aren't open when processing

### Error Handling

- Low confidence extractions (< 0.7) flagged for manual review
- Failed API calls logged with retry mechanism
- Malformed receipts moved to error folder
- Processing history maintained in `processing_log.json`

## Contributing

### Development Guidelines

1. **Commit Strategy**: Feature-based commits with descriptive messages
2. **Code Style**: Follow PEP 8 standards
3. **Testing**: Test with various receipt types before committing
4. **Documentation**: Update README for new features

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-functionality

# Make changes and commit
git add .
git commit -m "expense_tracker: Add new functionality"

# Push to main branch
git checkout main
git merge feature/new-functionality
git push origin main
```

## License

This project is for personal use. Contains proprietary financial data processing logic.

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review processing logs in `data/processing_log.json`
3. Verify API key configuration in `.env`

---
*Last Updated: June 2025*  
*Estimated Development Time: 3-4 weeks*  
*Monthly Operating Cost: <$2 SGD*