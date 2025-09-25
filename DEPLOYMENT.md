# Deployment Guide

## 🚀 Heroku Deployment Instructions

### Prerequisites
1. Install Heroku CLI from https://devcenter.heroku.com/articles/heroku-cli
2. Create a free Heroku account at https://heroku.com

### Step-by-Step Deployment

#### 1. Install Heroku CLI
```bash
# On macOS with Homebrew
brew tap heroku/brew && brew install heroku

# On Windows
# Download and run the installer from https://devcenter.heroku.com/articles/heroku-cli

# On Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

#### 2. Login to Heroku
```bash
heroku login
```

#### 3. Create Heroku App
```bash
heroku create your-app-name
# Replace 'your-app-name' with your desired app name
```

#### 4. Deploy to Heroku
```bash
git push heroku main
```

#### 5. Scale the App
```bash
heroku ps:scale web=1
```

#### 6. Open Your App
```bash
heroku open
```

### Alternative: Deploy via Heroku Dashboard

1. Go to https://dashboard.heroku.com
2. Click "New" → "Create new app"
3. Enter app name and choose region
4. Connect your GitHub repository
5. Enable automatic deploys
6. Click "Deploy branch"

### 🔧 Configuration Files

The following files are already configured for Heroku deployment:

- `Procfile`: Defines how to run the app
- `requirements.txt`: Python dependencies
- `runtime.txt`: Python version specification

### 📊 Monitoring

After deployment, you can monitor your app:

```bash
# View logs
heroku logs --tail

# Check app status
heroku ps

# View app info
heroku info
```

### 🌐 Your API URL

Once deployed, your API will be available at:
```
https://your-app-name.herokuapp.com
```

### 🧪 Testing the Deployed API

Test your deployed API with:

```bash
# Health check
curl https://your-app-name.herokuapp.com/

# Search example
curl -X POST "https://your-app-name.herokuapp.com/search" \
  -H "Content-Type: application/json" \
  -d '[{"length": 10, "quantity": 1}]'
```

### 💰 Cost Information

- **Free Tier**: 550-1000 hours/month (sufficient for testing)
- **Paid Plans**: Start at $7/month for always-on apps

### 🛠️ Troubleshooting

#### Common Issues:

1. **Build Failures**: Check that all dependencies are in `requirements.txt`
2. **App Crashes**: Check logs with `heroku logs --tail`
3. **Slow Response**: Apps sleep after 30 minutes of inactivity on free tier

#### Useful Commands:

```bash
# Restart the app
heroku restart

# Check app status
heroku ps:status

# View recent logs
heroku logs --tail --num 100
```

### 🔄 Updating Your App

To update your deployed app:

```bash
# Make changes to your code
git add .
git commit -m "Update description"
git push heroku main
```

---

**Note**: The first request to a sleeping Heroku app may take a few seconds due to cold start. Subsequent requests will be much faster.