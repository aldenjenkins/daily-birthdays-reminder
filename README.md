# DailyBirthdayReminders

-   Send out an email with a digest of a acquaintence's birthday's occurring today.

### Intuition

-   Remembering birthdays is incredibly valuable, but is very hard to do without automation.

### Usage

-   In a crontab:

```{bash}
SMTP_HOST=smtp.site.com SMTP_PASS=password EMAIL_FROM=from@test.com EMAIL_TO=to@test.com /the_dir/send_email.py

```
