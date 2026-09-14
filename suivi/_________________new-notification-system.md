# Fix silent error/success feedback:

Replace notificationState with notifyError / notifySuccess / notifyWarning / notifyInfo from [$lib/notifications.svelte](cronexia-gta-front-v2/app/src/lib/notifications.svelte.ts) (same pattern as admin fields pages).

Reference on @cronexia-gta-front-v2\app\src\routes\(app)\(with-filters)\employee-file\population\[[population]]\resource\[[resource]]\dateStart\[[dateStart]]\dateEnd\[[dateEnd]]\+page.svelte (10-15) , too

On form error, prefer the string error from the action (fail(..., { error: result.message })) over JSON.stringify(response).

Set creating = false on error paths as well as success.

Plan note: Split into mangeable steps
