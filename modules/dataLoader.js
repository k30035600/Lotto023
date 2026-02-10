/**
 * 데이터 로더 모듈
 * 로또 데이터 로드 및 캐싱 관리
 */

/**
 * LocalStorage 캐시 키
 */
const CACHE_KEYS = {
    LOTTO645: 'LOTTO645_DATA_CACHE',
    LOTTO023: 'LOTTO023_DATA_CACHE',
    METADATA: 'LOTTO_METADATA_CACHE'
};

/**
 * LocalStorage에서 데이터 가져오기
 * @param {string} key - 캐시 키
 * @returns {*|null} 캐시된 데이터 또는 null
 */
function getFromCache(key) {
    try {
        const cached = localStorage.getItem(key);
        if (cached) {
            return JSON.parse(cached);
        }
    } catch (error) {
        console.error(`캐시 읽기 오류 [${key}]:`, error);
    }
    return null;
}

/**
 * LocalStorage에 데이터 저장
 * @param {string} key - 캐시 키
 * @param {*} data - 저장할 데이터
 * @returns {boolean} 성공 여부
 */
function saveToCache(key, data) {
    try {
        localStorage.setItem(key, JSON.stringify(data));
        return true;
    } catch (error) {
        console.error(`캐시 저장 오류 [${key}]:`, error);
        // LocalStorage 용량 초과 시 오래된 캐시 삭제
        if (error.name === 'QuotaExceededError') {
            clearOldCache();
            try {
                localStorage.setItem(key, JSON.stringify(data));
                return true;
            } catch (retryError) {
                console.error('재시도 실패:', retryError);
            }
        }
    }
    return false;
}

/**
 * 오래된 캐시 삭제
 */
function clearOldCache() {
    try {
        // 메타데이터 제외하고 모든 캐시 삭제
        Object.values(CACHE_KEYS).forEach(key => {
            if (key !== CACHE_KEYS.METADATA) {
                localStorage.removeItem(key);
            }
        });
    } catch (error) {
        console.error('캐시 정리 오류:', error);
    }
}

/**
 * JSON 파일 로드
 * @param {string} url - JSON 파일 URL
 * @returns {Promise<Array>} 로드된 데이터
 */
async function loadJSON(url) {
    try {
        const timestamp = Date.now();
        const response = await fetch(`${url}?t=${timestamp}`);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        return Array.isArray(data) ? data : [];
    } catch (error) {
        console.error(`JSON 로드 오류 [${url}]:`, error);
        throw error;
    }
}

/**
 * XLSX 파일 로드 (SheetJS 사용)
 * @param {string} url - XLSX 파일 URL
 * @returns {Promise<Array>} 파싱된 데이터
 */
async function loadXLSX(url) {
    try {
        if (typeof XLSX === 'undefined') {
            throw new Error('XLSX 라이브러리가 로드되지 않았습니다.');
        }

        const timestamp = Date.now();
        const response = await fetch(`${url}?t=${timestamp}`);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const arrayBuffer = await response.arrayBuffer();
        const workbook = XLSX.read(arrayBuffer, { type: 'array' });
        const firstSheetName = workbook.SheetNames[0];

        if (!firstSheetName) {
            throw new Error('XLSX 파일에 시트가 없습니다.');
        }

        const sheet = workbook.Sheets[firstSheetName];
        const data = XLSX.utils.sheet_to_json(sheet, { defval: '' });

        return data;
    } catch (error) {
        console.error(`XLSX 로드 오류 [${url}]:`, error);
        throw error;
    }
}

/**
 * Lotto645 데이터 로드 (캐시 우선)
 * @param {string} basePath - 기본 경로
 * @returns {Promise<Array>} 로또 데이터
 */
async function loadLotto645Data(basePath = '') {
    console.time('LoadLotto645');

    // 1. 캐시 확인
    const cached = getFromCache(CACHE_KEYS.LOTTO645);
    if (cached && Array.isArray(cached) && cached.length > 0) {
        console.timeEnd('LoadLotto645');
        return cached.sort((a, b) => b.round - a.round);
    }

    // 2. JSON 로드 시도
    try {
        const jsonUrl = `${basePath}source/Lotto645.json`;
        const data = await loadJSON(jsonUrl);

        if (data.length > 0) {
            const sorted = data.sort((a, b) => b.round - a.round);
            saveToCache(CACHE_KEYS.LOTTO645, sorted);
            console.timeEnd('LoadLotto645');
            return sorted;
        }
    } catch (error) {
        console.warn('JSON 로드 실패, XLSX 시도:', error);
    }

    // 3. XLSX 로드 (fallback)
    try {
        const xlsxUrl = `${basePath}source/Lotto645.xlsx`;
        const data = await loadXLSX(xlsxUrl);

        if (data.length > 0) {
            const sorted = data.sort((a, b) => b.round - a.round);
            saveToCache(CACHE_KEYS.LOTTO645, sorted);
            console.timeEnd('LoadLotto645');
            return sorted;
        }
    } catch (error) {
        console.error('XLSX 로드 실패:', error);
    }

    console.timeEnd('LoadLotto645');
    return [];
}

/**
 * Lotto023 데이터 로드
 * @param {string} basePath - 기본 경로
 * @returns {Promise<Array>} 로또 데이터
 */
async function loadLotto023Data(basePath = '') {
    console.time('LoadLotto023');

    // 1. 캐시 확인
    const cached = getFromCache(CACHE_KEYS.LOTTO023);
    if (cached && Array.isArray(cached) && cached.length > 0) {
        console.timeEnd('LoadLotto023');
        return cached;
    }

    // 2. JSON 로드 시도
    try {
        const jsonUrl = `${basePath}source/Lotto023.json`;
        const data = await loadJSON(jsonUrl);

        if (data.length > 0) {
            saveToCache(CACHE_KEYS.LOTTO023, data);
            console.timeEnd('LoadLotto023');
            return data;
        }
    } catch (error) {
        console.warn('JSON 로드 실패, XLSX 시도:', error);
    }

    // 3. XLSX 로드 (fallback)
    try {
        const xlsxUrl = `${basePath}source/Lotto023.xlsx`;
        const data = await loadXLSX(xlsxUrl);

        if (data.length > 0) {
            saveToCache(CACHE_KEYS.LOTTO023, data);
            console.timeEnd('LoadLotto023');
            return data;
        }
    } catch (error) {
        console.error('XLSX 로드 실패:', error);
    }

    console.timeEnd('LoadLotto023');
    return [];
}

/**
 * API에서 최신 회차 정보 가져오기
 * @param {string} apiUrl - API URL
 * @returns {Promise<Object|null>} 최신 회차 데이터
 */
async function fetchLatestRound(apiUrl) {
    try {
        const response = await fetch(apiUrl);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('최신 회차 조회 오류:', error);
        return null;
    }
}

/**
 * 데이터 유효성 검증
 * @param {Array} data - 검증할 데이터
 * @param {string} type - 데이터 타입 ('lotto645' | 'lotto023')
 * @returns {boolean} 유효성 여부
 */
function validateData(data, type = 'lotto645') {
    if (!Array.isArray(data) || data.length === 0) {
        return false;
    }

    // 첫 번째 항목 검증
    const first = data[0];

    if (type === 'lotto645') {
        return first.round !== undefined &&
            first.numbers !== undefined &&
            Array.isArray(first.numbers) &&
            first.numbers.length === 6;
    }

    return true;
}

/**
 * 캐시 무효화
 * @param {string} [key] - 특정 키만 무효화, 없으면 전체
 */
function invalidateCache(key) {
    if (key) {
        localStorage.removeItem(key);
    } else {
        Object.values(CACHE_KEYS).forEach(k => {
            localStorage.removeItem(k);
        });
    }
}

// 전역으로 export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        CACHE_KEYS,
        getFromCache,
        saveToCache,
        clearOldCache,
        loadJSON,
        loadXLSX,
        loadLotto645Data,
        loadLotto023Data,
        fetchLatestRound,
        validateData,
        invalidateCache
    };
}
