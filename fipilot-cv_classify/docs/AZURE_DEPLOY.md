# Deploy Fipilot lên Azure

Kiến trúc đề xuất: hai Azure Container Apps (frontend và backend), Azure Container
Registry để lưu image, và Azure Database for PostgreSQL Flexible Server.

## 1. Chuẩn bị

Cài Azure CLI, đăng nhập và chọn subscription:

```bash
az login
az account set --subscription "TEN_SUBSCRIPTION"
```

Các lệnh dưới đây chạy từ thư mục gốc repository. Đổi các giá trị viết hoa trước
khi chạy.

## 2. Tạo tài nguyên dùng chung

```bash
az group create --name fipilot-rg --location southeastasia
az acr create --resource-group fipilot-rg --name FIPILOT_ACR_NAME --sku Basic
az containerapp env create --resource-group fipilot-rg --name fipilot-env --location southeastasia
az postgres flexible-server create \
  --resource-group fipilot-rg --name FIPILOT_DB_NAME \
  --location southeastasia --admin-user fipilotadmin \
  --admin-password 'DB_PASSWORD' --database-name fipilot \
  --sku-name Standard_B1ms --tier Burstable --public-access 0.0.0.0
```

Lấy chuỗi kết nối PostgreSQL từ Azure Portal, mục **Connection strings**, rồi
đổi sang dạng SQLAlchemy:

```text
postgresql+psycopg://fipilotadmin:DB_PASSWORD@FIPILOT_DB_NAME.postgres.database.azure.com:5432/fipilot?sslmode=require
```

## 3. Build và push image

```bash
az acr login --name FIPILOT_ACR_NAME
docker build -t FIPILOT_ACR_NAME.azurecr.io/fipilot-backend:latest ./backend
docker push FIPILOT_ACR_NAME.azurecr.io/fipilot-backend:latest
docker build -t FIPILOT_ACR_NAME.azurecr.io/fipilot-frontend:latest ./frontend
docker push FIPILOT_ACR_NAME.azurecr.io/fipilot-frontend:latest
```

## 4. Deploy backend trước

```bash
az containerapp create --resource-group fipilot-rg --name fipilot-backend \
  --environment fipilot-env --image FIPILOT_ACR_NAME.azurecr.io/fipilot-backend:latest \
  --target-port 8000 --ingress external --registry-server FIPILOT_ACR_NAME.azurecr.io \
  --min-replicas 1 --max-replicas 2 --cpu 2 --memory 4Gi \
  --env-vars DATABASE_URL='POSTGRES_CONNECTION_STRING' COOKIE_SECURE=true
```

Sau khi lệnh hoàn tất, lấy URL backend:

```bash
az containerapp show --resource-group fipilot-rg --name fipilot-backend \
  --query properties.configuration.ingress.fqdn -o tsv
```

Chạy migration một lần trong backend container hoặc Azure Cloud Shell:

```bash
az containerapp exec --resource-group fipilot-rg --name fipilot-backend \
  --command "/bin/sh"
alembic upgrade head
```

## 5. Deploy frontend

```bash
az containerapp create --resource-group fipilot-rg --name fipilot-frontend \
  --environment fipilot-env --image FIPILOT_ACR_NAME.azurecr.io/fipilot-frontend:latest \
  --target-port 3000 --ingress external --registry-server FIPILOT_ACR_NAME.azurecr.io \
  --min-replicas 1 --max-replicas 2 --cpu 1 --memory 2Gi \
  --env-vars RESUME_API_URL='https://BACKEND_FQDN'
```

Lấy URL public:

```bash
az containerapp show --resource-group fipilot-rg --name fipilot-frontend \
  --query properties.configuration.ingress.fqdn -o tsv
```

Mở URL đó trên trình duyệt. Không cần chạy `npm run dev` hoặc `uvicorn` trên máy
cá nhân nữa.

## Lưu ý quan trọng

- Không commit `DATABASE_URL`, API keys hoặc mật khẩu vào GitHub; khai báo chúng
  trong Azure Container App > **Secrets and environment variables**.
- Backend có các thư viện AI nặng và có thể cần tải YOLO model khi khởi động.
  Container backend nên bắt đầu với tối thiểu 4 GiB RAM.
- Nếu frontend build lỗi do giới hạn tài nguyên, build image trên máy local rồi
  push lên ACR như các lệnh trên.
