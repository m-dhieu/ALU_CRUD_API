# Setting Up GitHub Actions for Docker Hub Deployment

This guide will help you set up a GitHub Actions workflow that automatically builds and pushes your Docker image to Docker Hub whenever you commit to the master branch.

## Prerequisites

1. A GitHub account
2. A Docker Hub account
3. Your project with a valid Dockerfile

## Steps

### 1. Create Docker Hub Access Tokens

1. Log in to [Docker Hub](https://hub.docker.com/)
2. Go to Account Settings > Security
3. Create a new access token with appropriate permissions (Read & Write)
4. Copy the token value (you will only see it once!)

### 2. Add Secrets to Your GitHub Repository

1. Go to your GitHub repository
2. Navigate to Settings > Secrets and variables > Actions
3. Add the following secrets:
   - `DOCKERHUB_USERNAME` - Your Docker Hub username
   - `DOCKERHUB_TOKEN` - The access token you created

### 3. Create GitHub Actions Workflow File

Create a new file in your repository at `.github/workflows/docker-build-push.yml` with the following content:

```yaml
name: Build and Push Docker Image

on:
  push:
    branches:
      - main
      - master

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
        
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
        
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
          
      - name: Extract metadata for Docker
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ secrets.DOCKERHUB_USERNAME }}/moto-booking-api
          tags: |
            type=raw,value=latest
            type=sha,format=short
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=registry,ref=${{ secrets.DOCKERHUB_USERNAME }}/moto-booking-api:buildcache
          cache-to: type=registry,ref=${{ secrets.DOCKERHUB_USERNAME }}/moto-booking-api:buildcache,mode=max
```

### 4. Understanding the Versioning System

The workflow automatically tags your Docker image with:

- `latest` - Always points to the most recent build
- `sha-<commit>` - Short commit SHA (e.g., `sha-a1b2c3d`)
- When you create a tag/release with semantic versioning:
  - Full version (e.g., `1.0.0`)
  - Major.Minor version (e.g., `1.0`)

### 5. Creating Tagged Releases

To create a semantically versioned image:

1. Create a new tag in your repository:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
   
2. Or create a release through the GitHub web interface:
   - Go to your repository
   - Click on "Releases"
   - Click "Create a new release"
   - Enter a tag version (e.g., `v1.0.0`)
   - Publish the release

### 6. Verifying Your Workflow

After pushing to the master branch:

1. Go to the "Actions" tab in your GitHub repository
2. You should see your workflow running
3. Once completed, check your Docker Hub repository for the new images with appropriate tags

### 7. Using Specific Versions in Production

In your production deployment scripts, you can specify exact versions:

```bash
docker pull yourusername/moto-booking-api:1.0.0
```

Or use the short SHA for specific commits:

```bash
docker pull yourusername/moto-booking-api:sha-a1b2c3d
```

## Troubleshooting

- **Workflow fails at login**: Double-check your Docker Hub credentials in GitHub Secrets
- **Push permission denied**: Ensure your Docker Hub token has write permissions
- **Build fails**: Check if your Dockerfile is valid and all required files are included

## Advanced Configuration

You can customize the workflow further by:

- Adding environment variables
- Running tests before building
- Setting up multi-platform builds
- Adding conditional builds for different branches

For more information, refer to the [Docker GitHub Actions documentation](https://docs.docker.com/ci-cd/github-actions/).
