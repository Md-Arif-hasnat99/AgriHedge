# Contributing to AgriHedge

Thank you for your interest in contributing to AgriHedge! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/your-repo/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, Python version, Node version)

### Suggesting Features

1. Check if the feature has been suggested in [Issues](https://github.com/your-repo/issues)
2. Create a new issue with:
   - Clear feature description
   - Use case / problem it solves
   - Proposed solution
   - Alternative solutions considered

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Write/update tests
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 💻 Development Setup

### Backend Development

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Mobile Development

```powershell
cd mobile
npm install
npx expo start
```

## 📝 Code Style

### Python (Backend)
- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions/classes
- Format with `black`
- Lint with `flake8`

Example:
```python
from typing import List, Optional

def get_price_history(
    commodity: str,
    days: int = 30
) -> List[dict]:
    """
    Get historical price data for a commodity
    
    Args:
        commodity: Commodity name
        days: Number of days to fetch
        
    Returns:
        List of price records
    """
    # Implementation
    pass
```

### JavaScript/React (Mobile)
- Use ES6+ features
- Follow Airbnb style guide
- Use functional components and hooks
- Format with Prettier
- Lint with ESLint

Example:
```javascript
import React, { useState, useEffect } from 'react';

const PriceChart = ({ commodity, days = 30 }) => {
  const [data, setData] = useState([]);
  
  useEffect(() => {
    fetchPriceData(commodity, days).then(setData);
  }, [commodity, days]);
  
  return <Chart data={data} />;
};

export default PriceChart;
```

## 🧪 Testing

### Backend Tests

```powershell
cd backend
pytest tests/ -v --cov=app
```

### Mobile Tests

```powershell
cd mobile
npm test
```

## 📚 Documentation

- Update README.md if adding new features
- Add docstrings to Python code
- Add JSDoc comments to JavaScript code
- Update API documentation in OpenAPI spec

## 🔍 Code Review Process

1. All PRs require at least one review
2. Address review comments
3. Ensure CI/CD passes
4. Maintain test coverage above 80%

## 🌟 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Acknowledged in release notes
- Invited to join the core team (for significant contributions)

## 📧 Contact

- Email: dev@agrihedge.com
- Discord: [Join our server](https://discord.gg/agrihedge)
- GitHub Discussions: [Start a discussion](https://github.com/your-repo/discussions)

## ⚖️ Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Maintain professionalism

Thank you for contributing to AgriHedge! 🚀
