# Dev Container Validation Checklist

**Created**: 2024-12-13
**Status**: Pending validation after container rebuild

## After Rebuild - Run These Commands

### 1. Verify Docker-outside-of-Docker
```bash
docker --version
docker compose version
docker ps  # Should show host Docker containers
```

### 2. Verify Node.js & npm
```bash
node --version   # Should be v20.x
npm --version
```

### 3. Verify Python & uv
```bash
python3 --version  # Should be 3.12.x
uv --version
```

### 4. Verify Playwright Browsers Installed
```bash
npx playwright --version
ls ~/.cache/ms-playwright/  # Should show chromium, firefox, webkit
```

### 5. Run Playwright System Check
```bash
npx playwright install --dry-run  # Should say "all browsers installed"
```

### 6. Run Sample Test (headless)
```bash
npm run test:e2e -- tests/e2e/health.spec.ts --project=chromium
```
Expected: Tests will fail (app not running) but Playwright should launch without browser errors.

### 7. Verify Headed Mode Works
```bash
npm run test:e2e:headed -- tests/e2e/health.spec.ts --project=chromium
```
Expected: Browser window should open (may need X11 forwarding or VNC for remote).

## Known Issues to Watch For

| Issue | Symptom | Fix |
|-------|---------|-----|
| Browser crash | "Target closed" or SIGBUS | Increase `--shm-size` in devcontainer.json |
| Missing libs | "error while loading shared libraries" | Re-run `npx playwright install-deps` |
| Docker socket | "permission denied" on /var/run/docker.sock | Add user to docker group or check socket mount |

## Next Steps After Validation

1. [ ] Confirm all checks pass
2. [ ] Run `*ci` workflow to scaffold GitHub Actions
3. [ ] Begin Epic 1 implementation

---

**To resume TEA agent**: `/bmad:bmm:agents:tea` then select menu item or say "continue validation"
