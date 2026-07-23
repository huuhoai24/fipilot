import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';
var productionVariables = [
    'VITE_API_BASE_URL',
    'VITE_FIREBASE_API_KEY',
    'VITE_FIREBASE_AUTH_DOMAIN',
    'VITE_FIREBASE_PROJECT_ID',
    'VITE_FIREBASE_APP_ID',
];
export default defineConfig(function (_a) {
    var mode = _a.mode;
    var env = loadEnv(mode, process.cwd(), '');
    if (mode === 'production') {
        var localBuild = env.VITE_LOCAL_BUILD === 'true';
        var missing = productionVariables.filter(function (name) { var _a; return !((_a = env[name]) === null || _a === void 0 ? void 0 : _a.trim()); });
        if (missing.length) {
            throw new Error("Missing production environment variables: ".concat(missing.join(', ')));
        }
        if (!localBuild && !/^https:\/\//.test(env.VITE_API_BASE_URL)) {
            throw new Error('VITE_API_BASE_URL must use HTTPS in production');
        }
    }
    return {
        plugins: [react()],
        resolve: {
            alias: {
                '@': path.resolve(__dirname, './src'),
            },
        },
        server: {
            port: 5173,
        },
    };
});
