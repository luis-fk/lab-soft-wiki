import Showdown from "showdown";

const sd = new Showdown.Converter({
    tables: true,
    tasklists: true,
    strikethrough: true,
    emoji: true,
    simpleLineBreaks: true,
    openLinksInNewWindow: true,
    backslashEscapesHTMLTags: true,
    smoothLivePreview: true,
    simplifiedAutoLink: true,
    requireSpaceBeforeHeadingText: true,
    ghMentions: true,
    ghMentionsLink: '/user/{u}',
    ghCodeBlocks: true,
    underline: true,
    completeHTMLDocument: true,
    metadata: true,
    parseImgDimensions: true,
    encodeEmails: true
});

export default sd;