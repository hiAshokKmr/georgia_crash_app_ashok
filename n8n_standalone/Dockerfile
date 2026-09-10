FROM docker.n8n.io/n8nio/n8n:latest

USER root

# Install standard utilities if needed
RUN apk add --no-cache curl tzdata

# Set timezone for Georgia / Eastern Standard Time
ENV GENERIC_TIMEZONE=America/New_York
ENV TZ=America/New_York

# Give node user permissions
RUN mkdir -p /home/node/.n8n && chown -R node:node /home/node/.n8n

USER node
WORKDIR /home/node

EXPOSE 5678
CMD ["n8n", "start"]
