# Contributing to SkillSwap-Map

Thank you for your interest in contributing! We welcome contributions from everyone. This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions. We're committed to providing a welcoming and inspiring community.

## Getting Started

1. **Fork the repository**
2. **Clone your fork**
```bash
git clone https://github.com/yourusername/skillswap-map.git
cd skillswap-map
```

3. **Create a new branch**
```bash
git checkout -b feature/your-feature-name
# or for bug fixes
git checkout -b fix/your-bug-fix
```

4. **Set up development environment** (see SETUP.md)

## Branch Naming

Use descriptive branch names:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions
- `chore/` - Maintenance tasks

Example: `feature/add-video-chat` or `fix/messaging-notifications`

## Commit Guidelines

### Commit Message Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that don't affect code meaning
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding or updating tests
- `chore`: Changes to build process or dependencies

### Example
```
feat(messaging): add read receipts to messages

- Add is_read and read_at fields to Message model
- Implement read receipt API endpoint
- Update WebSocket to send read notifications

Closes #123
```

## Pull Request Process

1. **Update your branch**
```bash
git pull origin main
```

2. **Run tests and linting**

**Backend:**
```bash
docker-compose exec backend bash -c "flake8 . && python manage.py test"
```

**Frontend:**
```bash
docker-compose exec frontend npm run lint
```

3. **Make your changes**
   - Keep changes focused and atomic
   - Add tests for new features
   - Update documentation if needed

4. **Push your branch**
```bash
git push origin feature/your-feature-name
```

5. **Create Pull Request**
   - Use a clear, descriptive title
   - Reference related issues (e.g., "Closes #123")
   - Describe what changed and why
   - Include screenshots for UI changes

## Coding Standards

### Python (Backend)

**Style Guide:** PEP 8

**Tools:**
- `black` - Code formatter
- `flake8` - Linter

**Format code:**
```bash
black apps/
```

**Check style:**
```bash
flake8 apps/
```

**Guidelines:**
- Use meaningful variable names
- Write docstrings for functions and classes
- Keep functions small and focused
- Use type hints where possible
- Write comments for complex logic

**Example:**
```python
def get_nearby_skills(user_latitude: float, user_longitude: float, radius_km: int = 50) -> QuerySet:
    """
    Find skills available within a given radius of user's location.
    
    Args:
        user_latitude: User's current latitude
        user_longitude: User's current longitude
        radius_km: Search radius in kilometers (default: 50)
    
    Returns:
        QuerySet of Skill objects
    """
    # Implementation here
    pass
```

### JavaScript/React (Frontend)

**Style Guide:** Airbnb JavaScript Style Guide

**Tools:**
- `eslint` - Linter
- `prettier` - Code formatter

**Format code:**
```bash
npm run format
```

**Check style:**
```bash
npm run lint
```

**Guidelines:**
- Use functional components with hooks
- Keep components small and reusable
- Use descriptive variable names
- Add comments for complex logic
- Use proper error handling

**Example:**
```javascript
const SkillCard = ({ skill, onLike }) => {
  const [isLoading, setIsLoading] = useState(false);

  const handleLike = async () => {
    setIsLoading(true);
    try {
      await api.likeSkill(skill.id);
      onLike(skill.id);
    } catch (error) {
      console.error('Error liking skill:', error);
      toast.error('Failed to like skill');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="skill-card">
      {/* Component JSX */}
    </div>
  );
};
```

## Testing

### Backend Tests

**Write tests for:**
- API endpoints
- Model methods
- Service functions
- Utility functions

**Run tests:**
```bash
python manage.py test
# or specific app
python manage.py test apps.users
```

**Example:**
```python
from django.test import TestCase
from apps.users.models import User

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('testpass123'))
```

### Frontend Tests

**Write tests for:**
- Components
- Hooks
- Utility functions
- API integration

**Run tests:**
```bash
npm test
```

## Documentation

### Docstrings (Python)

Use Google-style docstrings:

```python
def function_name(arg1: str, arg2: int) -> bool:
    """
    Brief description of what function does.
    
    Longer description explaining the function in more detail if needed.
    Can span multiple lines and explain the rationale.
    
    Args:
        arg1: Description of arg1
        arg2: Description of arg2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When something is invalid
    
    Example:
        >>> function_name("hello", 42)
        True
    """
    pass
```

### Comments (General)

- Explain the "why", not the "what"
- Keep comments up-to-date
- Use clear, concise language
- Avoid over-commenting obvious code

## Database Migrations

When modifying models:

1. **Create migration**
```bash
docker-compose exec backend python manage.py makemigrations
```

2. **Review migration file** - Ensure it's correct

3. **Test migration**
```bash
docker-compose exec backend python manage.py migrate
```

4. **Include migration in PR** - Commit migration files

## Issue Reporting

### Before Opening an Issue

- Check existing issues to avoid duplicates
- Test with the latest code
- Gather relevant information

### Issue Template

```markdown
## Description
Clear description of the issue

## Steps to Reproduce
1. First step
2. Second step
3. Expected behavior
4. Actual behavior

## Environment
- OS: [e.g., macOS, Windows, Linux]
- Browser: [if applicable]
- Version: [commit hash or version number]

## Additional Context
Screenshots, logs, or other relevant information
```

## Feature Requests

### Feature Request Template

```markdown
## Description
Clear description of the feature

## Motivation
Why would this be useful?

## Proposed Solution
How do you envision this working?

## Alternatives
Have you considered alternative approaches?

## Additional Context
Mockups, examples, or references
```

## Review Process

1. **Code Review**
   - At least one approval required
   - All checks must pass
   - No conflicts with main branch

2. **Testing**
   - All tests must pass
   - New features should have tests
   - Coverage should not decrease

3. **Documentation**
   - Updated if necessary
   - Clear and accurate

## Release Process

Maintainers will handle releases. Follow semantic versioning:
- MAJOR: Incompatible API changes
- MINOR: Backward-compatible functionality added
- PATCH: Backward-compatible bug fixes

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project website

## Questions?

- 💬 Open a discussion on GitHub
- 📧 Email: contribute@skillswap-map.com
- 💭 Join our Discord community

Thank you for contributing to SkillSwap-Map! 🎉
