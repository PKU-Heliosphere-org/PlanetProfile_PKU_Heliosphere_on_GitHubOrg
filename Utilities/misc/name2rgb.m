function [varargout]=name2rgb(name)
%NAME2RGB    Converts short/long color names to RGB triplets
%
%    Usage:    rgb=name2rgb(name)
%              [longname,rgb]=name2rgb()
%              name2rgb()
%
%    Description:
%     RGB=NAME2RGB(NAME) converts short/long color names to red-green-blue
%     triplet values.  NAME must be a string or a cell array of strings.
%     RGB is a Nx3 array of triplets corresponding to the color names in
%     NAME.  See the third usage format for a list of all 700+ color names.
%
%     [LONGNAME,RGB]=NAME2RGB() returns a cell array of all color names in
%     LONGNAME and their respective red-green-blue values in RGB.
%
%     NAME2RGB() prints out a list of color names and their corresponding
%     red-green-blue values.
%
%    Notes:
%     - 'bl' is assumed to be 'blue' as Matlab does
%     - Supports an extended set of color names:
%       SHORTNAME   LONGNAME         RGB
%       r           red              [1   0   0  ]
%       o           orange           [1   0.5 0  ]
%       y           yellow           [1   1   0  ]
%       l           lawngreen        [0.5 1   0  ]
%       g           green            [0   1   0  ]
%       s           springgreen      [0   1   0.5]
%       c           cyan             [0   1   1  ]
%       a           azure            [0   0.5 1  ]
%       b           blue             [0   0   1  ]
%       v           violet           [0.5 0   1  ]
%       m           magenta          [1   0   1  ]
%       f           flower or rose   [1   0   0.5]
%       k           black            [0   0   0  ]
%       w           white            [1   1   1  ]
%
%    Examples:
%     % Make a colormap with all valid shortnames:
%     colormap(name2rgb(('roylgscabvmfkw')'));
%
%     % A colorful plot:
%     fh=figure('color',name2rgb('royal blue'));
%     ax=axes('parent',fh,'color',name2rgb('purple'),'nextplot','add',...
%          'xcolor',name2rgb('unmellow yellow'),'ycolor',name2rgb('mint'));
%     plot(rand(100,10),rand(100,10),'.','parent',ax);
%
%    See also: INVERTCOLOR, COLORMAP

%     Version History:
%        May  11, 2010 - initial version
%        Feb. 23, 2011 - altered some color names, added extending color
%                        name list (now over 700 colors!), new options
%        Feb. 25, 2011 - drop shortname short circuit due to false
%                        positives (ie 'gray')
%
%     Written by Garrett Euler (ggeuler at wustl dot edu)
%     Last Updated Feb. 25, 2011 at 12:00 GMT

% todo:

% check nargin
error(nargchk(0,1,nargin));

% valid short names
%sn='roylgacsbvmpkw';
sn_rgb=[1 0 0; 1 .5 0; 1 1 0; .5 1 0; 0 1 0; 0 1 .5; 0 1 1; 0 .5 1; 0 0 1;
    .5 0 1; 1 0 1; 1 0 .5; 0 0 0; 1 1 1];

% cell string of long+short names
ln={'r' 'o' 'y' 'l' 'g' 's' 'c' 'a' 'b' 'v' 'm' 'f' 'k' 'w' ...
    'red' 'orange' 'yellow' 'lawngreen' 'green' 'springgreen' 'cyan' ...
    'azure' 'blue' 'violet' 'magenta' 'flower' 'black' 'white'};
ln_rgb=[sn_rgb; sn_rgb];

% extended colors
en={... % a
    'air force blue' 'alice blue' 'alizarin' 'almond' 'amaranth' ...
    'amber' 'amber sae' 'american rose' 'amethyst' 'anti-flash white' ...
    'antique brass' 'antique fuchsia' 'antique white' 'ao' 'ao english' ...
    'apple green' 'apricot' 'aqua' 'aquamarine' 'army green' ...
    'arsenic' 'arylide yellow' 'ash grey' 'asparagus' 'atomic tangerine' ...
    'auburn' 'aureolin' 'aurometalsaurus' 'awesome' 'azure' ...
    'azure mist' ...
    ... % b
    'baby blue' 'baby blue eyes' 'baby pink' 'ball blue' 'banana mania' ...
    'banana yellow' 'battleship grey' 'bazaar' 'beau blue' 'beaver' ...
    'beige' 'bisque' 'bistre' 'bittersweet' 'black' ...
    'blanched almond' 'bleu de france' 'blizzard blue' 'blond' 'blue' ...
    'blue munsell' 'blue ncs' 'blue pigment' 'blue ryb' 'blue bell' ...
    'blue gray' 'blue-green' 'blue-violet' 'blush' 'bole' ...
    'bondi blue' 'boston university red' 'brandeis blue' 'brass' 'brick red' ...
    'bright cerulean' 'bright green' 'bright lavender' 'bright maroon' 'bright pink' ...
    'bright turquoise' 'bright ube' 'brilliant lavender' 'brilliant rose' 'brink pink' ...
    'british racing green' 'bronze' 'brown' 'brown web' 'bubble gum' ...
    'bubbles' 'buff' 'bulgarian rose' 'burgundy' 'burlywood' ...
    'burnt orange' 'burnt sienna' 'burnt umber' 'byzantine' 'byzantium' ...
    ... % c
    'cadet' 'cadet blue' 'cadet grey' 'cadmium green' 'cadmium orange' ...
    'cadmium red' 'cadmium yellow' 'cal poly pomona green' 'cambridge blue' 'camel' ...
    'camouflage green' 'canary yellow' 'candy apple red' 'candy pink' 'capri' ...
    'caput mortuum' 'cardinal' 'caribbean green' 'carmine' 'carmine pink' ...
    'carmine red' 'carnation pink' 'carnelian' 'carolina blue' 'carrot orange' ...
    'ceil' 'celadon' 'celestial blue' 'cerise' 'cerise pink' ...
    'cerulean' 'cerulean blue' 'chamoisee' 'champagne' 'charcoal' ...
    'chartreuse yellow' 'chartreuse green' 'cherry blossom pink' 'chestnut' 'chocolate' ...
    'chocolate web' 'chrome yellow' 'cinereous' 'cinnabar' 'cinnamon' ...
    'citrine' 'classic rose' 'cobalt' 'cocoa brown' 'columbia blue' ...
    'cool black' 'cool grey' 'copper' 'copper rose' 'coquelicot' ...
    'coral' 'coral pink' 'coral red' 'cordovan' 'corn' ...
    'cornell red' 'cornflower blue' 'cornsilk' 'cosmic latte' 'cotton candy' ...
    'cream' 'crimson' 'crimson glory' 'cyan' 'cyan process' ...
    ... %d
    'daffodil' 'dandelion' 'dark blue' 'dark brown' 'dark byzantium' ...
    'dark candy apple red' 'dark cerulean' 'dark champagne' 'dark chestnut' 'dark coral' ...
    'dark cyan' 'dark electric blue' 'dark goldenrod' 'dark gray' 'dark green' ...
    'dark jungle green' 'dark khaki' 'dark lava' 'dark lavender' 'dark magenta' ...
    'dark midnight blue' 'dark olive green' 'dark orange' 'dark orchid' 'dark pastel blue' ...
    'dark pastel green' 'dark pastel purple' 'dark pastel red' 'dark pink' 'dark powder blue' ...
    'dark raspberry' 'dark red' 'dark salmon' 'dark scarlet' 'dark sea green' ...
    'dark sienna' 'dark slate blue' 'dark slate gray' 'dark spring green' 'dark tan' ...
    'dark tangerine' 'dark taupe' 'dark terra cotta' 'dark turquoise' 'dark violet' ...
    'dartmouth green' 'davys grey' 'debian red' 'deep carmine' 'deep carmine pink' ...
    'deep carrot orange' 'deep cerise' 'deep champagne' 'deep chestnut' 'deep fuchsia' ...
    'deep jungle green' 'deep lilac' 'deep magnenta' 'deep peach' 'deep pink' ...
    'deep saffron' 'deep sky blue' 'denim' 'desert' 'desert sand' ...
    'dim gray' 'dodger blue' 'dogwood rose' 'dollar bill' 'drab' ...
    'duke blue' ...
    ... %e
    'earth yellow' 'ecru' 'eggplant' 'eggshell' 'egyptian blue' ...
    'electric blue' 'electric crimson' 'electric cyan' 'electric green' 'electric indigo' ...
    'electric lavender' 'electric lime' 'electric purple' 'electric ultramarine' 'electric violet' ...
    'electric yellow' 'emerald' 'eton blue' ...
    ... % f
    'fallow' 'falu red' 'fandango' 'fashion fuchsia' 'fawn' ...
    'feldgrau' 'fern green' 'ferrari red' 'field drab' 'firebrick' ...
    'fire engine red' 'flame' 'flamingo pink' 'flavescent' 'flax' ...
    'floral white' 'fluorescent orange' 'fluorescent pink' 'fluorescent yellow' 'folly' ...
    'forest green' 'forest green web' 'french beige' 'french blue' 'french lilac' ...
    'french rose' 'fuchsia' 'fuchsia pink' 'fulvous' 'fuzzy wuzzy' ...
    ... % g
    'gainsboro' 'gamboge' 'ghost white' 'ginger' 'glaucous' ...
    'gold' 'golden' 'golden brown' 'golden poppy' 'golden yellow' ...
    'goldenrod' 'granny smith apple' 'gray' 'gray x11' 'gray-asparagus' ...
    'green' 'green medium' 'green munsell' 'green ncs' 'green pigment' ...
    'green ryb' 'green-yellow' 'grullo' 'guppie green' ...
    ... % h
    'halaya ube' 'han blue' 'han purple' 'hansa yellow' 'harlequin' ...
    'harvard crimson' 'harvest gold' 'heart gold' 'hellotrope' 'hollywood cerise' ...
    'honeydew' 'hookers green' 'hot magenta' 'hot pink' 'hunter green' ...
    ... % i
    'iceberg' 'icterine' 'inchworm' 'india green' 'indian red' ...
    'indian yellow' 'indigo dye' 'indigo web' 'international klein blue' 'international orange' ...
    'iris' 'isabelline' 'islamic green' 'ivory' ...
    ... % j
    'jade' 'jasper' 'jasmine' 'jazzberry jam' 'jonquil' ...
    'june bud' 'jungle green' ...
    ... % k
    'kelly green' 'khaki' 'khaki light' ...
    ... % l
    'la salle green' 'languid lavender' 'lapis lazuli' 'laser lemon' 'lava' ...
    'lavender' 'lavender web' 'lavender blue' 'lavender blush' 'lavender gray' ...
    'lavender indigo' 'lavender magenta' 'lavender mist' 'lavender pink' 'lavender purple' ...
    'lavender rose' 'lawn green' 'lemon' 'lemon chiffon' 'light apricot' ...
    'light blue' 'light brown' 'light carmine pink' 'light coral' 'light cornflower blue' ...
    'light crimson' 'light cyan' 'light fuchsia pink' 'light goldenrod yellow' 'light gray' ...
    'light green' 'light khaki' 'light mauve' 'light pastel purple' 'light pink' ...
    'light salmon' 'light salmon pink' 'light sea green' 'light sky blue' 'light slate gray' ...
    'light taupe' 'light thulian pink' 'light yellow ' 'lilac' 'lime' ...
    'lime web' 'lime green' 'lincoln green' 'linen' 'liver' ...
    'lust' ...
    ... % m
    'macaroni and cheese' 'magenta' 'magenta dye' 'magenta process' 'magic mint' ...
    'magnolia' 'mahogany' 'maize' 'majorelle blue' 'malachite' ...
    'manatee' 'mango tango' 'maroon' 'maroon x11' 'mauve' ...
    'mauve taupe' 'mauvelous' 'maya blue' 'meat brown' 'medium aquamarine' ...
    'medium blue' 'medium candy apple red' 'medium carmine' 'medium champagne' 'medium electric blue' ...
    'medium jungle green' 'medium lavender magenta' 'medium orchid' 'medium persian blue' 'medium purple' ...
    'medium red-violet' 'medium sea green' 'medium slate blue' 'medium spring bud' 'medium spring green' ...
    'medium taupe' 'medium teal blue' 'medium turquoise' 'medium violet-red' 'melon' ...
    'midnight blue' 'midnight green' 'mikado yellow' 'mint' 'mint cream' ...
    'mint green' 'misty rose' 'moccasin' 'mode beige' 'moonstone blue' ...
    'mordant red 19' 'moss green' 'mountain meadow' 'mountbatten pink' 'mulberry' ...
    'mustard' 'myrtle' 'msu green' ...
    ... % n
    'nadeshiko pink' 'napier green' 'naples yellow' 'navajo white' 'navy blue' ...
    'neon carrot' 'neon fuchsia' 'neon green' 'non-photo blue' ...
    ... % o
    'ocean boat blue' 'ochre' 'office green' 'old gold' 'old lace' ...
    'old lavender' 'old mauve' 'old rose' 'olive' 'olive drab' ...
    'olive drab #7' 'olivine' 'onyx' 'opera mauve' 'orange' ...
    'orange ryb' 'orange web' 'orange peel' 'orange-red' 'orchid' ...
    'otter brown' 'outer space' 'outrageous orange' 'oxford blue' 'ou crimson red' ...
    ... % p
    'pakistan green' 'palatinate blue' 'palatinate purple' 'pale aqua' 'pale blue' ...
    'pale brown' 'pale carmine' 'pale cerulean' 'pale chestnut' 'pale copper' ...
    'pale cornflower blue' 'pale gold' 'pale goldenrod' 'pale green' 'pale magenta' ...
    'pale pink' 'pale plum' 'pale red-violet' 'pale robin egg blue' 'pale silver' ...
    'pale silver bud' 'pale taupe' 'pale violet-red' 'pansy purple' 'papaya whip' ...
    'paris green' 'pastel blue' 'pastel brown' 'pastel gray' 'pastel green' ...
    'pastel magenta' 'pastel orange' 'pastel pink' 'pastel purple' 'pastel red' ...
    'pastel violet' 'pastel yellow' 'patriarch' 'paynes grey' 'peach' ...
    'peach-orange' 'peach puff' 'peach-yellow' 'pear' 'pearl' ...
    'pearl aqua' 'peridot' 'periwinkle' 'persian blue' 'persian green' ...
    'persian indigo' 'persian orange' 'persian pink' 'persian plum' 'persian red' ...
    'persian rose' 'persimmon' 'phlox' 'phthalo blue' 'phthalo green' ...
    'piggy pink' 'pine green' 'pink' 'pink-orange' 'pink pearl' ...
    'pink sherbet' 'pistachio' 'platinum' 'plum' 'plum web' ...
    'portland orange' 'powder blue' 'princeton orange' 'prune' 'prussian blue' ...
    'psychedelic purple' 'puce' 'pumpkin' 'purple' 'purple munsell' ...
    'purple x11' 'purple heart' 'purple mountain majesty' 'purple pizzazz' 'purple taupe' ...
    ... % q (none)
    ... % r
    'radical red' 'raspberry' 'raspberry glace' 'raspberry pink' 'raspberry rose' ...
    'raw umber' 'razzle dazzle rose' 'razzmatazz' 'red' 'red munsell' ...
    'red ncs' 'red pigment' 'red ryb' 'red-brown' 'red-violet' ...
    'redwood' 'regalia' 'rich black' 'rich brilliant lavender' 'rich carmine' ...
    'rich electric blue' 'rich lavender' 'rich lilac' 'rich maroon' 'rifle green' ...
    'robin egg blue' 'rose' 'rose bonbon' 'rose ebony' 'rose gold' ...
    'rose madder' 'rose pink' 'rose quartz' 'rose taupe' 'rose vale' ...
    'rosewood' 'rosso corsa' 'rosy brown' 'royal azure' 'royal blue' ...
    'royal blue web' 'royal fuchsia' 'royal purple' 'ruby' 'ruddy' ...
    'ruddy brown' 'ruddy pink' 'rufous' 'russet' 'rust' ...
    ... % s
    'sacramento state green' 'saddle brown' 'safety orange' 'saffron' 'st. patricks blue' ...
    'salmon' 'salmon pink' 'sand' 'sand dune' 'sandstorm' ...
    'sandy brown' 'sandy taupe' 'sangria' 'sap green' 'sapphire' ...
    'satin sheen gold' 'scarlet' 'school bus yellow' 'screamin green' 'sea green' ...
    'seal brown' 'seashell' 'selective yellow' 'sepia' 'shadow' ...
    'shamrock green' 'shocking pink' 'sienna' 'silver' 'sinopia' ...
    'skobeloff' 'sky blue' 'sky magenta' 'slate blue' 'slate gray' ...
    'smalt' 'smokey topaz' 'smoky black' 'snow' 'spiro disco ball' ...
    'splashed white' 'spring bud' 'spring green' 'steel blue' 'stil de grain yellow' ...
    'stizza' 'straw' 'sunglow' 'sunset' ...
    ... % t
    'tan' 'tangelo' 'tangerine' 'tangerine yellow' 'taupe' ...
    'taupe gray' 'tea green' 'tea rose' 'tea rose orange' 'teal' ...
    'teal blue' 'teal green' 'tenne' 'terra cotta' 'thistle' ...
    'thulian pink' 'tickle me pink' 'tiffany blue' 'tigers eye' 'timberwolf' ...
    'titanium yellow' 'tomato' 'toolbox' 'tractor red' 'trolley grey' ...
    'tropical rain forest' 'true blue' 'tufts blue' 'tumbleweed' 'turkish rose' ...
    'turquoise' 'turquoise blue' 'turquoise green' 'tuscan red' 'twilight lavender' ...
    'tyrian purple' ...
    ... % u
    'ua blue' 'ua red' 'ube' 'ucla blue' 'ucla gold' ...
    'ufo green' 'ultramarine' 'ultramarine blue' 'ultra pink' 'umber' ...
    'united nations blue' 'unmellow yellow' 'up forest green' 'up maroon' 'upsdell red' ...
    'urobilin' 'usc cardinal' 'usc gold' 'utah crimson' ...
    ... % v
    'vanilla' 'vegas gold' 'venetian red' 'verdigris' 'vermilion' ...
    'veronica' 'violet' 'violet 400nm' 'violet ryb' 'violet web' ...
    'viridian' 'vivid auburn' 'vivid burgundy' 'vivid cerise' 'vivid tangerine' ...
    'vivid violet' ...
    ... % w
    'warm black' 'wenge' 'wheat' 'white' 'white smoke' ...
    'wild blue yonder' 'wild strawberry' 'wild watermelon' 'wine' 'wisteria' ...
    ... % x
    'xanadu' ...
    ... % y
    'yale blue' 'yellow' 'yellow munsell' 'yellow ncs' 'yellow process' ...
    'yellow ryb' 'yellow-green' ...
    ... % z
    'zaffre' 'zinnwaldite brown' ...
    };
en_rgb=[... % a
        36 54 66; 94 97 100; 82 10 26; 94 87 80; 90 17 31;
        100 75 0; 100 49 0; 100 1 24; 60 40 80; 95 95 96;
        80 58 46; 57 36 51; 98 92 84; 0 0 100; 0 50 0;
        55 71 0; 98 81 69; 0 100 100; 50 100 83; 29 33 13;
        23 27 29; 91 84 42; 70 75 71; 53 66 42; 100 60 40;
        43 21 10; 99 93 0; 43 50 50; 100 13 32; 0 50 100;
        94 100 100; ...
        ... % b
        51 81 94; 63 79 95; 96 76 76; 13 67 80; 98 91 71; 
        100 88 21; 52 52 51; 60 47 48; 74 83 90; 62 51 44; 
        96 96 86; 100 89 77; 24 17 12; 100 44 37; 0 0 0; 
        100 92 80; 19 55 91; 67 90 93; 98 94 75; 0 0 100; 
        0 50 69; 0 53 74; 20 20 60; 1 28 100; 64 64 82;
        40 60 80; 0 87 87; 54 17 89; 87 36 51; 47 27 23;
        0 58 71; 80 0 0; 0 44 100; 71 65 26; 80 25 33;
        11 67 84; 40 100 0; 75 58 89; 76 13 28; 100 0 50;
        3 91 87; 82 62 91; 96 73 100; 100 33 64; 98 38 50;
        0 26 15; 80 50 20; 59 29 0; 65 16 16; 99 76 80;
        91 100 100; 94 86 51; 28 2 3; 50 0 13; 87 72 53;
        80 33 0; 91 45 32; 54 20 14; 74 20 64; 44 16 39;
        ... %c
        33 41 47; 37 62 63; 57 64 69; 0 42 24; 93 53 18;
        89 0 13; 100 96 0; 12 30 17; 64 76 68; 76 60 42;
        47 53 42; 100 94 0; 100 3 0; 89 44 48; 0 75 100;
        35 15 13; 77 12 23; 0 80 60; 59 0 9; 92 30 26;
        100 0 22; 100 65 79; 70 11 11; 60 73 89; 93 57 13;
        57 63 81; 67 88 69; 29 59 82; 87 19 39; 93 23 51;
        0 48 65; 16 32 75; 63 47 35; 97 91 81; 21 27 31;
        87 100 0; 50 100 0; 100 72 77; 80 36 36; 48 25 0;
        82 41 12; 100 65 0; 60 51 48; 89 26 20; 82 41 12;
        89 82 4; 98 80 91; 0 28 67; 82 41 12; 61 87 100;
        0 18 39; 55 57 67; 72 45 20; 60 40 40; 100 22 0;
        100 50 31; 97 51 47; 100 25 25; 54 25 27; 98 93 36;
        70 11 11; 39 58 93; 100 97 86; 100 97 91; 100 74 85;
        100 99 82; 86 8 24; 75 0 20; 0 100 100; 0 72 92;
        ... % d
        100 100 19; 94 88 19; 0 0 55; 40 26 13; 36 22 33;
        64 0 0; 3 27 49; 76 70 50; 60 41 38; 80 36 27;
        0 55 55; 33 41 47; 72 53 4; 66 66 66; 0 20 13;
        10 14 13; 74 72 42; 28 24 20; 45 31 59; 55 0 55;
        0 20 40; 33 42 18; 100 55 0; 60 20 80; 47 62 80;
        1 75 24; 59 44 84; 76 23 13; 91 33 50; 0 20 60;
        53 15 34; 55 0 0; 91 59 48; 34 1 10; 56 74 56;
        24 8 8; 28 24 55; 18 31 31; 9 45 27; 57 51 32;
        100 66 7; 28 24 20; 80 31 36; 0 81 82; 58 0 83;
        5 50 6; 33 33 33; 84 4 33; 66 13 24; 94 19 22;
        91 41 17; 85 20 53; 98 84 65; 73 31 28; 76 33 76;
        0 29 29; 60 33 73; 80 0 80; 100 80 64; 100 8 58;
        100 60 20; 0 75 100; 8 38 74; 76 60 42; 93 79 69;
        41 41 41; 12 56 100; 84 9 41; 52 73 40; 59 44 9;
        0 0 61;
        ... % e
        88 66 37; 76 70 50; 38 25 32; 94 92 84; 6 20 65;
        49 98 100; 100 0 25; 0 100 100; 0 100 0; 44 0 100;
        96 73 100; 80 100 0; 75 0 100; 25 0 100; 56 0 100;
        100 100 0; 31 78 47; 59 78 64;
        ... % f
        76 60 42; 50 9 9; 71 20 54; 96 0 63; 90 67 44;
        30 36 33; 31 47 26; 100 11 0; 42 33 12; 70 13 13;
        81 9 13; 89 35 13; 99 56 67; 97 91 56; 93 86 51;
        100 98 94; 100 75 0; 100 8 58; 80 100 0; 100 0 31;
        0 27 13; 13 55 13; 65 48 36; 0 45 73; 53 38 56;
        96 29 54; 100 0 100; 100 47 100; 86 52 0; 80 40 40;
        ... % g
        86 86 86; 89 61 6; 97 97 100; 69 40 0; 38 51 71;
        83 69 22; 100 84 0; 60 40 8; 99 76 0; 100 87 0;
        85 65 13; 66 89 63; 50 50 50; 75 75 75; 27 35 27;
        0 100 0; 0 50 0; 0 66 47; 0 62 42; 0 65 31;
        40 69 20; 68 100 18; 66 60 53; 0 100 50;
        ... % h
        40 22 33; 27 42 81; 32 9 98; 91 84 42; 25 100 0;
        79 0 9; 85 57 0; 50 50 0; 87 45 100; 96 0 63;
        94 100 94; 0 44 0; 100 11 81; 100 41 71; 21 37 23;
        ... % i
        44 65 82; 99 97 37; 70 93 36; 7 53 3; 80 36 36;
        89 66 34; 0 25 42; 29 0 51; 0 18 65; 100 31 0;
        35 31 81; 96 94 93; 0 56 0; 100 100 94;
        ... % j
        0 66 42; 84 23 24; 97 87 49; 65 4 37; 98 85 37;
        74 85 34; 16 67 53;
        ... % k
        30 73 9; 76 69 57; 94 90 55;
        ... % l
        3 47 19; 84 79 87; 15 38 61; 100 100 13; 81 6 13;
        71 49 86; 90 90 98; 80 80 100; 100 94 96; 77 76 82;
        58 34 92; 93 51 93; 90 90 98; 98 68 82; 59 48 71;
        98 63 89; 49 99 0; 100 97 0; 100 98 80; 99 84 69;
        68 85 90; 71 40 11; 90 40 38; 94 50 50; 60 81 93;
        96 41 57; 88 100 100; 98 52 94; 98 98 82; 83 83 83;
        56 93 56; 94 90 55; 86 82 100; 69 61 85; 100 71 76;
        100 63 48; 100 60 60; 13 70 67; 53 81 98; 47 53 60;
        70 55 43; 90 56 67; 100 100 88; 78 64 78; 75 100 0;
        0 100 0; 20 80 20; 11 35 2; 98 94 90; 33 29 31;
        90 13 13;
        ... % m
        100 74 53; 100 0 100; 79 8 48; 100 0 56; 67 94 82;
        97 96 100; 75 25 0; 98 93 37; 38 31 86; 4 85 32;
        59 60 67; 100 51 26; 50 0 0; 69 19 38; 88 69 100;
        57 37 43; 94 60 67; 45 76 98; 90 72 23; 40 80 67;
        0 0 80; 89 2 17; 69 25 21; 95 90 67; 1 31 59;
        11 21 18; 80 60 80; 73 33 83; 0 40 65; 58 44 86;
        73 20 52; 24 70 44; 48 41 93; 79 86 54; 0 98 60;
        40 30 28; 0 33 71; 28 82 80; 78 8 52; 99 74 71;
        10 10 44; 0 29 33; 100 77 5; 24 71 54; 96 100 98;
        60 100 60; 100 89 88; 98 92 84; 59 44 9; 45 66 76;
        68 5 0; 68 87 68; 19 73 56; 60 48 55; 77 29 55;
        100 86 35; 13 26 12; 9 27 23;
        ... % n
        96 68 78; 16 50 0; 98 85 37; 100 87 68; 0 0 50;
        100 64 26; 100 25 39; 22 88 8; 64 87 93;
        ... % o
        0 47 75; 80 47 13; 0 50 0; 81 71 23; 99 96 90;
        47 41 47; 40 19 28; 75 50 51; 50 50 0; 42 56 14;
        24 20 12; 60 73 45; 6 6 6; 72 52 65; 100 50 0;
        98 60 1; 100 65 0; 100 62 0; 100 27 0; 85 44 84;
        40 26 13; 25 29 30; 100 43 29; 0 13 28; 60 0 0;
        ... % p
        0 40 0; 15 23 89; 41 16 38; 74 83 90; 69 93 93;
        60 46 33; 69 25 21; 61 77 89; 87 68 69; 85 54 40;
        67 80 94; 90 75 54; 93 91 67; 60 98 60; 98 52 90;
        98 85 87; 80 60 80; 86 44 58; 59 87 82; 79 75 73;
        93 92 74; 74 60 49; 86 44 58; 47 9 29; 100 94 84;
        31 78 47; 68 78 81; 51 41 33; 81 81 77; 47 87 47;
        96 60 76; 100 70 28; 100 82 86; 70 62 71; 100 41 38;
        80 60 79; 99 99 59; 50 0 50; 25 25 28; 100 90 71;
        100 80 60; 100 85 73; 98 87 68; 82 89 19; 94 92 84;
        53 85 75; 90 89 0; 80 80 100; 11 22 73; 0 65 58;
        20 7 48; 85 56 35; 97 50 75; 44 11 11; 80 20 20;
        100 16 64; 93 35 0; 87 0 100; 0 6 54; 7 21 14;
        99 87 90; 0 47 44; 100 75 80; 100 60 40; 91 67 81;
        97 56 65; 58 77 45; 90 89 89; 56 27 52; 80 60 80;
        100 35 21; 69 88 90; 100 56 0; 44 11 11; 0 19 33;
        87 0 100; 80 53 60; 100 46 9; 50 0 50; 62 0 77;
        63 36 94; 41 21 61; 59 47 71; 100 31 85; 31 25 30;
        ... % q (none)
        ... % r
        100 21 37; 89 4 36; 57 37 43; 89 31 61; 70 27 42;
        51 40 27; 100 20 80; 89 15 42; 100 0 0; 95 0 24;
        77 1 20; 93 11 14; 100 15 7; 65 16 16; 78 8 52;
        67 31 32; 32 18 50; 0 25 25; 95 65 100; 84 0 25;
        3 57 82; 67 38 80; 71 40 82; 69 19 38; 25 28 20;
        0 80 80; 100 0 50; 98 26 62; 40 30 28; 72 43 47;
        89 15 21; 100 40 80; 67 60 66; 56 36 36; 67 31 32;
        40 0 4; 83 0 0; 74 56 56; 0 22 66; 0 14 40;
        25 41 88; 79 17 57; 47 32 66; 88 7 37; 100 0 16;
        73 40 16; 88 56 59; 66 11 3; 50 27 11; 72 25 5;
        ... % s
        0 34 25; 55 27 7; 100 40 0; 96 77 19; 14 16 48;
        100 55 41; 100 57 64; 76 70 50; 59 44 9; 93 84 25;
        96 64 38; 59 44 9; 57 0 4; 31 49 16; 3 15 40;
        80 63 21; 100 14 0; 100 85 0; 46 100 44; 18 55 34;
        20 8 8; 100 96 93; 100 73 0; 44 26 8; 54 47 36;
        0 62 38; 99 6 75; 53 18 9; 75 75 75; 80 25 4;
        0 48 45; 53 81 92; 81 44 69; 42 35 80; 44 50 56;
        0 20 60; 58 25 3; 6 5 3; 100 98 98; 6 75 99;
        100 99 100; 65 99 0; 0 100 50; 27 51 71; 98 85 37;
        60 0 0; 89 85 44; 100 80 20; 98 84 65;
        ... % t
        82 71 55; 98 30 0; 95 52 0; 100 80 0; 28 24 20;
        55 52 54; 82 94 75; 97 51 47; 96 76 76; 0 50 50;
        21 46 53; 0 51 50; 80 34 0; 89 45 36; 85 75 85;
        87 44 63; 99 54 67; 4 73 71; 88 55 24; 86 84 82;
        93 90 0; 100 39 28; 45 42 75; 99 5 21; 50 50 50;
        0 46 37; 0 45 81; 28 57 81; 87 67 53; 71 45 51;
        19 84 78; 0 100 94; 63 84 71; 51 21 21; 54 29 42;
        40 1 24;
        ... % u
        0 20 67; 85 0 30; 53 47 76; 33 41 58; 100 70 0;
        24 82 44; 7 4 56; 25 40 96; 100 44 100; 39 32 28;
        36 57 90; 100 100 40; 0 27 13; 48 7 7; 68 9 13;
        88 68 13; 60 0 0; 100 80 0; 83 0 25;
        ... % v
        95 90 67; 77 70 35; 78 3 8; 26 70 68; 89 26 20;
        63 36 94; 50 0 100; 56 0 100; 53 0 69; 93 51 93;
        25 51 43; 58 15 14; 62 11 21; 85 11 51; 100 63 54;
        62 0 100;
        ... % w
        0 26 26; 39 33 32; 96 87 70; 100 100 100; 96 96 96;
        64 68 82; 100 26 64; 99 42 52; 45 18 22; 79 63 86;
        ... % x
        45 53 47;
        ... % y
        6 30 57; 100 100 0; 94 80 0; 100 83 0; 100 94 0;
        100 100 20; 60 80 20;
        ... % z
        0 8 66; 17 9 3;
        ]./100;
ln=[ln en];
ln_rgb=[ln_rgb; en_rgb];

% no input case
if(~nargin)
    if(nargout)
        varargout={ln ln_rgb};
    else
        % print it all
        for i=1:numel(ln)
            fprintf('%24s = [%4g %4g %4g]\n',ln{i},ln_rgb(i,:))
        end
    end
    return;
end

% convert name to cellstr
if(ischar(name)); name=cellstr(name); end
if(iscellstr(name))
    %long/short names in cells
    % - using strmatch so we catch partial names
    % - in case of blue/black conflict, choose blue like matlab
    varargout{1}=nan(numel(name),3);
    for i=1:numel(name)
        idx=strmatch(name{i},ln);
        if(isempty(idx))
            error('seizmo:name2rgb:badName',...
                'Unknown Color: %s',name{:});
        end
        varargout{1}(i,:)=ln_rgb(idx(1),:);
    end
else
    error('seizmo:name2rgb:badName',...
        'NAME must be a string or a cell array of strings!');
end

end
