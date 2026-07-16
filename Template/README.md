# Question Templates

Bộ mẫu câu hỏi phỏng vấn AI theo vị trí và cấp độ kinh nghiệm.

## Cấp độ kinh nghiệm

| Level | Kinh nghiệm |
|-------|-------------|
| `level_1` | 0–1 năm |
| `level_2` | 1–3 năm |
| `level_3` | 4–5 năm |
| `level_4` | 6–8 năm |
| `level_5` | 8+ năm |

## Cấu trúc thư mục

Mỗi vị trí có 5 level; mỗi level chứa 10 file câu hỏi (`01.md`–`10.md`):

- 3 câu dễ (`01.md`–`03.md`)
- 4 câu trung bình (`04.md`–`07.md`)
- 3 câu khó (`08.md`–`10.md`)

## Danh sách vị trí

| Thư mục | Vị trí |
|---------|--------|
| `web_developer/` | Web Developer |
| `backend_developer/` | Back-End Developer |
| `software_engineer/` | Software Engineer |
| `full_stack_developer/` | Full-Stack Developer |
| `data_engineer/` | Data Engineer |
| `data_scientist/` | Data Scientist |
| `ai_engineer/` | AI Engineer |
| `tester_qa_qc/` | Tester / QA / QC |
| `devops_engineer/` | DevOps Engineer |
| `business_analyst/` | Business Analyst |


## Định dạng file câu hỏi

Mỗi file `.md` chứa một câu hỏi và đáp án mẫu:

```markdown
# Câu hỏi

[Nội dung câu hỏi]

## Đáp án mẫu

[Nội dung đáp án ngắn gọn, chính xác]

## Metadata

- difficulty: easy | medium | hard
- tags: [tag1, tag2]
```
