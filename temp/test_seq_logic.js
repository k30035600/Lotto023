
function checkSequence(sortedNumbers, filterVal) {
    if (filterVal === 'none') {
        let seqCount = 0;
        for (let i = 1; i < sortedNumbers.length; i++) {
            if (sortedNumbers[i] === sortedNumbers[i - 1] + 1) seqCount++;
        }
        return seqCount === 0;
    }

    let seqCount = 0;
    for (let i = 1; i < sortedNumbers.length; i++) {
        if (sortedNumbers[i] === sortedNumbers[i - 1] + 1) seqCount++;
    }

    const target = parseInt(filterVal);
    return seqCount === target;
}

// 테스트 케이스
const cases = [
    { name: "3연번 (11,12,13)", nums: [11, 12, 13, 20, 30, 40], filter: '2' }, // 예상: 통과 (11-12, 12-13 => 2쌍)
    { name: "따로 2연번 (1,2, 4,5)", nums: [1, 2, 4, 5, 10, 20], filter: '2' },   // 예상: 통과 (1-2, 4-5 => 2쌍)
    { name: "4연번 (11,12,13,14)", nums: [11, 12, 13, 14, 30, 40], filter: '3' }, // 예상: 통과 (11-12, 12-13, 13-14 => 3쌍)
    { name: "2연번 (11,12)", nums: [11, 12, 20, 30, 40, 45], filter: '2' }        // 예상: 실패 (1쌍뿐임)
];

console.log("--- 연속 필터 로직 검증 ---");
cases.forEach(c => {
    const result = checkSequence(c.nums, c.filter);
    console.log(`[${c.name}] 번호:${c.nums} / 설정:${c.filter}회 -> 결과: ${result ? 'PASS' : 'FAIL'} (맞음)`);
});
