# Kiro Setup

## Requirements
- [Terraform Install](https://developer.hashicorp.com/terraform/install)
- [AWS CLI Install](https://awscli.amazonaws.com/AWSCLIV2.msi) & Profile Setup (`aws configure`)

## 1. uv Install
**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 2. Validation
```powershell
uvx awslabs.terraform-mcp-server@latest --help
```

## 3. Setup MCP
`C:\Users\<사용자명>\.kiro\settings\mcp.json`

```json
{
  "mcpServers": {
    "aws-terraform": {
      "command": "C:\\Users\\<사용자명>\\.local\\bin\\uvx.exe",
      "args": [
        "awslabs.terraform-mcp-server@latest"
      ],
      "env": {
        "AWS_PROFILE": "<Profile>"
      }
    }
  }
}
```
## 주의
-`command`는 `uvx`가 아닌 절대경로로 지정해야 PATH 인식 문제를 방지할 수 있습니다. </br>
- 설정 저장 후 Kiro CLI를 재시작해야 MCP 서버가 연결됨
