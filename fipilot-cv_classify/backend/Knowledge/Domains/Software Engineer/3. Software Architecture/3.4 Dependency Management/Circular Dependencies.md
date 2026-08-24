# Circular Dependencies

- A phụ thuộc B và B phụ thuộc A trực tiếp hoặc gián tiếp
- Làm initialization, testing và evolution khó khăn
- Giải bằng extracting abstraction, moving responsibility hoặc event/message boundary
- Không che cycle bằng service locator
