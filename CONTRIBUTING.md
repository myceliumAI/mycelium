# Contributing to Mycelium

First off, thank you for considering contributing to Mycelium! It's people like you that make Mycelium such a great tool. 

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Development Setup](#development-setup)
- [Development Process](#development-process)
- [Pull Request Process](#pull-request-process)
- [Project Structure](#project-structure)
- [Style Guidelines](#style-guidelines)
- [Testing](#testing)
- [Documentation](#documentation)

## 🤝 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to [maintainers@mycelium.ai].

## 🛠️ Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/mycelium.git
   cd mycelium
   ```

2. **Environment Setup**
   ```bash
   make setup     # Creates .env file from template
   make check     # Verifies all dependencies
   ```

3. **Launch Development Environment**
   ```bash
   make launch-dev
   ```

## 🔄 Development Process

1. **Create a Branch**
   ```bash
   git checkout -b feat/your-feature-name
   # or
   git checkout -b fix/your-fix-name
   ```

2. **Make Your Changes**
   - Write clean, maintainable code
   - Follow the style guidelines
   - Add tests for new features
   - Update documentation as needed

3. **Verify Your Changes**
   ```bash
   make test           # Run all tests
   make lint           # Check code style
   make format         # Format code
   ```

## 🔍 Pull Request Process

1. **Before Submitting**
   - [ ] Update documentation
   - [ ] Add/update tests
   - [ ] Run full test suite
   - [ ] Format code
   - [ ] Update changelog if needed

2. **Submitting**
   - Fill in the pull request template
   - Link any relevant issues
   - Request review from maintainers

3. **After Submitting**
   - Respond to review comments
   - Make requested changes
   - Rebase if needed

## 📁 Project Structure

```
mycelium/
├── backend/           # Backend services
│   ├── api/          # FastAPI application
│   ├── database/     # PostgreSQL setup
│   └── keycloak/     # Authentication service
├── mycelium/         # Frontend Vue.js application
├── docs/             # Documentation
└── scripts/          # Utility scripts
```

## 📝 Style Guidelines

### Python (Backend)
- Use type hints
- Follow PEP 8
- Use docstrings for functions and classes
- Format with Ruff

Example:
```python
def clean(self, client_name: str, delete_all: bool) -> Dict[str, Any]:
    """
    Deletes duplicate resources for a given client.

    :param str client_name: The name of the target client.
    :param bool delete_all: Determines the extent of deletion.
    :return Dict[str, Any]: The status response
    """
```

### Vue.js (Frontend)
- Follow Vue.js Style Guide
- Use TypeScript
- Use Composition API
- Format with ESLint/Prettier

## 🧪 Testing

### Backend Testing
```bash
make test-back
make test-back-coverage  # With coverage report
```

### Frontend Testing
```bash
make test-front
```

## 📚 Documentation

- Update README.md for major changes
- Document new features in `/docs`
- Include JSDoc comments for frontend components
- Add docstrings to Python functions

## 🚀 Available Commands

See all available commands:
```bash
make help
```

Common commands:
```bash
make launch-dev     # Start development environment
make test          # Run all tests
make lint          # Check code style
make format        # Format code
make clean         # Clean up resources
```

## ❓ Questions?

- Create a GitHub Discussion for general questions

## 📜 License

By contributing, you agree that your contributions will be licensed under the AGPL-3.0 License.

---
