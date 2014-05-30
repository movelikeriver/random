/**
 * The approach:
 * 1) do segmentation for the input Pinyin name;
 * 2) get Pinyin to IPA mapping for each initial and final, including some spacial case handling.
 */

function processKeyDown(event) {
	if(event.keyCode == 13) {
		lookUp();
	}
}

function lookUp() {
	output('');
	var pinyin = document.getElementById('name').value.trim().toLowerCase();

	if (!isValidInput(pinyin)) {
		output('Note: the input should be pure "a"-"z", no space, -, _, \', digit or other signs is allowed.  If you already know the segmentation, you can input the terms one by one.');
		return;
	}
	
	var syPairListGroup = doSegment(pinyin);
	if (syPairListGroup.length == 0) {
		output('invalid Pinyin name');
		return;
	}
	var strList = [];
	for (var i = 0; i < syPairListGroup.length; ++i) {
		var syPairList = syPairListGroup[i];
		var subList = [];
		var validPronCombination = true;
		for (var j = 0; j < syPairList.length; ++j) {
			var syPair = syPairList[j];
			var pron = getPron(syPair.s, syPair.y);
			if (pron.length == '') {
				validPronCombination = false;
				break;
			}
			subList.push(pron);			
		}
		if (validPronCombination == 0) {
			// this combination is incorrect.
			continue;
		}
		strList.push('(' + subList.join(', ') + ')<br/>');
	}
	output(strList.join(''));
}

/**
 * Display the result on the page.
 * @param {string} str: the string to be shown.
 */
function output(str) {
	document.getElementById('dbg').innerHTML = str;
}

/**
 * @type {Array} of 'yuan' (vowel), 'sheng' (Syllable initial), 'yun' (Syllable final)
 * @const
 */
var YUAN_LIST = {'a':true, 'e':true, 'i':true, 'o':true, 'u':true};
var SHENG_LIST = {
	'b':'b', 'p':'p', 'm':'m', 'f':'f', 'd':'d', 't':'t', 'n':'n', 'l':'l',
	'g':'g', 'k':'k', 'h':'h', 'j':'dʒ', 'q':'tʃ', 'x': 'ʃ',
	'zh':'dʒ', 'ch':'tʃ', 'sh':'ʃ', 'r':'r',
	'z':'z', 'c':'ts', 's':'s', 'y':'j', 'w':'w'};

// true means the 'yun' can be an independent term without 'sheng'.
var YUN_LIST = {
  'a':['a:', true], 'o':['ɔː', false], 'e':['ɜː', true], 'er':['ɜːr', true],
  'i':['i:', false], 'u':['u:', false], 'u2': ['ʒu:', false],
  'ai':['ai:', true], 'ei':['ei:', true], 'ui':['ui:', false],
  'ao':['au:', true], 'ou':['əʊ:', true], 'iu':['iəʊ:', false],
  'an':['a:n', true], 'en':['ɜːn', true], 'in':['i:n', false], 'un':['u:n', false], 'u2n': ['ʒuɜːn', false],
  'ang':['a:ŋ', true], 'eng':['ɜːŋ', true], 'ing':['i:ŋ', false], 'ong':['ɔːŋ', false],
  'ia':['ia:', false], 'ie':['ie:', false], 'iao':['iau:', false],
  'ian':['ie:n', false], 'iang':['ia:ŋ', false], 'iong':['iɔːŋ', false],
  'ua':['ua:', false], 'uan':['ua:n', false], 'u2an':['ʒua:n', false], 'uang':['ua:ŋ', false],
  'uo':['uɔː', false], 'ue': ['ʒuɜː', false], 'u2e': ['ʒuɜː', false],
};

function doSegment(input) {
	if (typeof input === 'undefined' || input.length == 0) {
		return [];
	}
	var retList = [];
	var syrList = cutFirstTerm(input);
	if (syrList.length == 0) {
		return [];
	}
	for (var i = 0; i < syrList.length; ++i) {
		var syr = syrList[i];
		if (syr.r.length == 0) {
			// find the last term.
			retList.push([{'s': syr.s, 'y': syr.y}]);
			continue;
		}
		var subSyListGroup = doSegment(syr.r);
		for (var j = 0; j < subSyListGroup.length; ++j) {
			var subSyList = subSyListGroup[j];
			retList.push([{'s': syr.s, 'y': syr.y}].concat(subSyList));
		}
	}
	return retList;
}

/**
 * @param {string} input
 * @return {Array} of {'s', 'y', 'r'}.
 */
function cutFirstTerm(input) {
	var retList = [];
	var idx = findFirstYuan(input);
	if (idx == -1) {
		return [];
	}
	var remainLength = Math.min(input.length - idx, 4);
	for (var len = 1; len <= remainLength; ++len) {
		var yun = input.substr(idx, len);
		if (!isValidYun(yun)) {
			continue;
		}
		var sheng = input.substr(0, idx);
		if (idx == 0) {
			sheng = '';
		}
		if (!isValidSheng(sheng)) {
			continue;
		}
		var remain = input.substr(idx + len);
		retList.push({'s': sheng, 'y': yun, 'r': remain});
	}
	return retList;
}

/**
 * Find the first YUAN letter.
 * Return -1 if not found.
 */
function findFirstYuan(input) {
	for (var i = 0; i < input.length; ++i) {
		if (input.charAt(i) in YUAN_LIST) {
			return i;
		}
	}
	return -1;
}

function isValidYun(yun) {
	if (yun in YUN_LIST) {
		return true;
	}
	return false;
}

function isValidSheng(sheng) {
	if (sheng.length == 0 || sheng in SHENG_LIST) {
		return true;
	}
	return false;
}

/**
 * @param {string}
 * @return {Boolean} true if the input contains pure latin letter.
 */
function isValidInput(input) {
	return /^[a-z]+$/i.test(input);
}

/**
 * @param {string} sheng
 * @param {string} yun
 * @return {string} the formatted name and pronunciation.
 */
function getPron(sheng, yun) {
	var pronYunPair = YUN_LIST[yun];
	if (sheng == '' && !pronYunPair[1]) {
		return '';
	}

	var name = (sheng == '' ? '' : sheng + '-') + yun;

	if (sheng == 'l' && yun == 'u') {
		// special case: lu and lv
		var pron = (' [' +
					SHENG_LIST[sheng] + YUN_LIST[yun][0] + '] or [' +
					SHENG_LIST[sheng] + YUN_LIST['u2'][0] + ']');
		return name + pron;
	}

	var pronSheng = (sheng == '' ? '' : SHENG_LIST[sheng]);
	var pronYun = pronYunPair[0];

	// other special cases:
	if (yun.charAt(0) == 'u') {
		// j, q, x, y + u
		var SPECIAL_U_SHENG_LIST = {'j': true, 'q': true, 'x': true, 'y': true};
		if (sheng in SPECIAL_U_SHENG_LIST) {
			var yun2 = yun.replace('u', 'u2');
			if (YUN_LIST[yun2] === undefined) {
				return '';
			}
			pronYun = YUN_LIST[yun2][0];
		}
	} else if (yun.charAt(0) == 'i' && sheng == 'y') {
		// y + i
		pronSheng = '';
	} else if (yun == 'ia') {
		var SPECIAL_IA_SHENG_LIST = {'j': true, 'q': true, 'x': true, 'd': true};
		if (SPECIAL_IA_SHENG_LIST[sheng] === undefined) {
			return '';
		}
	} else if (yun == 'er') {
		if (sheng != '') {
			return '';
		}
	} else if (yun == 'i') {
		var SPECIAL_I_SHENG_LIST = {
			'zh': true, 'ch': true, 'sh': true, 'r': true,
			'z': true, 'c': true, 's': true};
		
		if (sheng in SPECIAL_I_SHENG_LIST) {
			pronYun = '';
		}
	}

	var pron = pronSheng + pronYun;
	return name + ' [' + pron + ']';
}
