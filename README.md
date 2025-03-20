# Gerry AI - Twitch Chat Bot Suite

A collection of AI-powered Twitch chat bots with various functionalities including stock ticker display, text-to-speech, and OBS integration.

## Features

- Multiple AI-powered chat bots (WSB, BG3, Claude, DeepSeek, GerryAI)
- Real-time stock ticker display
- Text-to-speech responses
- OBS integration for visual effects
- Modular design for easy bot selection

## Prerequisites

- Docker and Docker Compose installed
- Twitch OAuth token
- OpenAI API key
- Anthropic API key (for Claude)
- ElevenLabs API key
- OBS WebSocket server (optional)

## Quick Start with Docker

1. Clone the repository:

```bash
git clone https://github.com/yourusername/gerry-ai.git
cd gerry-ai
```

2. Create a `config` directory and add your `keys.env` file:

```bash
mkdir config
```

3. Add your environment variables to `config/keys.env`:

```env
TWITCH_OAUTH_TOKEN=your_twitch_token
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
ELEVENLABS_API_KEY=your_elevenlabs_key
WEBSOCKET_HOST=localhost
WEBSOCKET_PORT=4455
WEBSOCKET_PASSWORD=your_password
```

4. Build and start the Docker container:

```bash
cd docker
docker-compose up --build
```

5. Access the ticker display at `http://localhost:8000/tickertape.html`

## Docker Commands

- Start the container:

```bash
cd docker
docker-compose up
```

- Start in detached mode (background):

```bash
cd docker
docker-compose up -d
```

- Stop the container:

```bash
cd docker
docker-compose down
```

- View logs:

```bash
cd docker
docker-compose logs -f
```

- Rebuild the container:

```bash
cd docker
docker-compose up --build
```

## Project Structure

```
gerry-ai/
├── bots/                 # Bot implementations
├── config/              # Configuration files
├── data/               # Data storage
│   └── audiobackup/    # Audio file backups
├── docker/             # Docker configuration files
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .dockerignore
├── tests/              # Test files
├── utilities/          # Utility modules
├── main.py            # Main entry point
├── requirements.txt   # Python dependencies
├── README.md         # Project documentation
└── LICENSE          # MIT License
```

## Available Bots

- **WSBbot**: WallStreetBets themed bot with stock ticker
- **BG3bot**: Baldur's Gate 3 themed bot
- **ClaudeBot**: Anthropic's Claude powered bot
- **DeepSeekBot**: DeepSeek AI powered bot
- **GerryAI**: General purpose AI bot

## Troubleshooting

### Docker Issues

1. If the container fails to start, check the logs:

```bash
cd docker
docker-compose logs
```

2. If you need to rebuild from scratch:

```bash
cd docker
docker-compose down
docker system prune -a
docker-compose up --build
```

3. If the ticker doesn't display:

- Ensure port 8000 is not in use
- Check if the container is running: `docker ps`
- Verify the logs for any errors

### Audio Issues

If you experience audio problems:

1. Ensure your system's audio device is properly configured
2. Check if the container has access to your audio device
3. Verify the ElevenLabs API key is valid

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- TradingView for the stock ticker widget
- TwitchIO for the Twitch chat integration
- OpenAI, Anthropic, and DeepSeek for AI capabilities
- ElevenLabs for text-to-speech
