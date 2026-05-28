# Ngày 1 — Bài Tập & Phản Ánh
## Nền Tảng LLM API | Phiếu Thực Hành

**Thời lượng:** 1:30 giờ  
**Cấu trúc:** Lập trình cốt lõi (60 phút) → Bài tập mở rộng (30 phút)

---

## Phần 1 — Lập Trình Cốt Lõi (0:00–1:00)

Chạy các ví dụ trong Google Colab tại: https://colab.research.google.com/drive/172zCiXpLr1FEXMRCAbmZoqTrKiSkUERm?usp=sharing

Triển khai tất cả TODO trong `template.py`. Chạy `pytest tests/` để kiểm tra tiến độ.

**Điểm kiểm tra:** Sau khi hoàn thành 4 nhiệm vụ, chạy:
```bash
python template.py
```
Bạn sẽ thấy output so sánh phản hồi của GPT-4o và GPT-4o-mini.

---

## Phần 2 — Bài Tập Mở Rộng (1:00–1:30)

### Bài tập 2.1 — Độ Nhạy Của Temperature
Gọi `call_openai` với các giá trị temperature 0.0, 0.5, 1.0 và 1.5 sử dụng prompt **"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> Khi temperature tăng dần từ 0.0 lên 1.5, các câu trả lời chuyển từ trạng thái an toàn, rập khuôn, mang tính xác thực cao sang trạng thái ngày càng đa dạng và sáng tạo hơn về mặt từ ngữ. Tuy nhiên, khi chạm đến ngưỡng quá cao (như 1.5), tính ngẫu nhiên lấn át khiến mô hình bị mất kiểm soát, dễ sinh ra các câu văn lủng củng, lạc đề hoặc bịa đặt thông tin sai sự thật (hallucination).

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> Đối với chatbot hỗ trợ khách hàng, tôi sẽ đặt temperature ở mức rất thấp, khoảng 0.0 đến 0.2. Trong dịch vụ chăm sóc khách hàng, sự chính xác, nhất quán và đáng tin cậy là ưu tiên hàng đầu. Ở mức nhiệt độ thấp, mô hình sẽ luôn bám sát vào các luồng thông tin có xác suất đúng cao nhất, từ đó ngăn chặn tuyệt đối rủi ro chatbot tự ý "sáng tạo" ra các chính sách hoàn tiền ảo hoặc báo sai giá sản phẩm gây thiệt hại cho doanh nghiệp.

---

### Bài tập 2.2 — Đánh Đổi Chi Phí
Xem xét kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người thực hiện 3 lần gọi API, mỗi lần trung bình ~350 token.

**Ước tính xem GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này:**
> Phân tích bài toán:

> Tổng số token sinh ra mỗi ngày: 10.000 (người) * 3 (cuộc gọi) * 350 (token) = 10.500.000 tokens.

> Dựa trên bảng giá trong file code (gpt-4o: $0.010 / 1K tokens | gpt-4o-mini: $0.0006 / 1K tokens):

> Chi phí chạy GPT-4o: (10.500.000 / 1.000) * 0.010 = $105 / ngày.

> Chi phí chạy GPT-4o-mini: (10.500.000 / 1.000) * 0.0006 = $6.3 / ngày.

> Kết luận: GPT-4o đắt hơn GPT-4o-mini khoảng 16.67 lần (105 / 6.3). Số tiền tiết kiệm được nếu dùng bản mini lên tới gần $3.000/tháng.

**Mô tả một trường hợp mà chi phí cao hơn của GPT-4o là xứng đáng, và một trường hợp GPT-4o-mini là lựa chọn tốt hơn:**
> GPT-4o hoàn toàn xứng đáng: Khi xây dựng các hệ thống đòi hỏi tư duy logic phức tạp, viết code phần mềm, phân tích hợp đồng pháp lý, hoặc xử lý các bài toán suy luận nhiều bước (Agentic workflows). Sự chênh lệch về trí thông minh ở các tác vụ khó này sẽ bù đắp hoàn toàn cho mức giá cao.

> GPT-4o-mini là lựa chọn tốt hơn: Khi cần xử lý dữ liệu số lượng lớn với các tác vụ đơn giản, lặp đi lặp lại như: tóm tắt bài báo, trích xuất dữ liệu từ văn bản thô (Data Extraction), phân loại email (Spam/Not Spam), hoặc các chatbot hỏi đáp thông thường (FAQ).

---

### Bài tập 2.3 — Trải Nghiệm Người Dùng với Streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì non-streaming lại phù hợp hơn?** (1 đoạn văn)
> Streaming quan trọng nhất: Trong các ứng dụng tương tác trực tiếp với con người (như Chatbot, UI/UX trên web). Các mô hình ngôn ngữ lớn thường mất nhiều giây để sinh ra một đoạn văn dài. Streaming giúp in từng chữ ra màn hình ngay lập tức, làm giảm thời gian chờ đợi nhận thức (Time To First Byte), giữ chân người dùng không bị rời đi vì tưởng ứng dụng bị "treo".

> Non-streaming phù hợp hơn: Khi sử dụng AI làm các công việc chạy ngầm (Background Processing). Ví dụ: Gọi API để AI sinh ra một chuỗi JSON, lưu kết quả dịch thuật vào Database, hoặc tự động kiểm duyệt bình luận. Trong các trường hợp này, máy tính (hoặc các hàm code tiếp theo) cần đợi AI hoàn thiện 100% cấu trúc dữ liệu rồi mới có thể bóc tách (parse) và xử lý tiếp được.


## Danh Sách Kiểm Tra Nộp Bài
- [ ] Tất cả tests pass: `pytest tests/ -v`
- [ ] `call_openai` đã triển khai và kiểm thử
- [ ] `call_openai_mini` đã triển khai và kiểm thử
- [ ] `compare_models` đã triển khai và kiểm thử
- [ ] `streaming_chatbot` đã triển khai và kiểm thử
- [ ] `retry_with_backoff` đã triển khai và kiểm thử
- [ ] `batch_compare` đã triển khai và kiểm thử
- [ ] `format_comparison_table` đã triển khai và kiểm thử
- [ ] `exercises.md` đã điền đầy đủ
- [ ] Sao chép bài làm vào folder `solution` và đặt tên theo quy định 
