const apiUrl = "https://7rf3jp6b97.execute-api.eu-central-1.amazonaws.com/prod/tagesthemen/json"
const DEBUG = false

const log = DEBUG ? console.log.bind(console) : function () { };

await createDirectory()

const widget = await createWidget()

// preview the widget
if (!config.runsInWidget) {
    await widget.presentSmall()
}

Script.setWidget(widget)
Script.complete()

async function createDirectory() {
    let fm = FileManager.local()

    let scriptPath = module.filename
    let libraryDir = scriptPath.replace(fm.fileName(scriptPath, true), fm.fileName(scriptPath, false))

    if (fm.fileExists(libraryDir) && !fm.isDirectory(libraryDir)) {
        fm.remove(libraryDir)
    }
    
    if (!fm.fileExists(libraryDir)) {
        fm.createDirectory(libraryDir)
    }
}

async function createWidget() {
    let data
    
    try {
        let r = new Request(apiUrl)

        r.headers = {
            "User-Agent": "Scriptable.app",
            "isPhone": Device.isPhone(),
            "isPad": Device.isPad()
        }
      
        data = await r.loadJSON()
    } catch(err) {
        const errorList = new ListWidget()
        errorList.addText("API nicht erreichbar.")
        return errorList
    }

    log("data: " + JSON.stringify(data, null, 2))

    logo = await getLogo(config.debug)

    //=== Create Widget =====================================
    const widget = new ListWidget()
    widget.backgroundColor = Color.white()
    widget.setPadding(20, 10, 40, 10)

    // === Logo =============================================
    let rowLogo = widget.addStack()
    rowLogo.layoutHorizontally()
    rowLogo.centerAlignContent()
    rowLogo.addSpacer()

    const tagesthemenLogoImg = rowLogo.addImage(logo)
    tagesthemenLogoImg.imageSize = new Size(130, 30)

    rowLogo.addSpacer()

    widget.addSpacer()

    //=== Time ==============================================
    let rowTime = widget.addStack()
    rowTime.layoutHorizontally()
    rowTime.centerAlignContent()
    rowTime.addSpacer()

    const timeText = rowTime.addText(data.when)
    timeText.centerAlignText()
    timeText.font = Font.heavySystemFont(30)
    timeText.textColor = new Color("#00134A")

    rowTime.addSpacer()

    return widget
}

async function getLogo(forceDownload) {
    let fm = FileManager.local()
    let scriptPath = module.filename
    let libraryDir = scriptPath.replace(fm.fileName(scriptPath, true), fm.fileName(scriptPath, false))
    let path = fm.joinPath(libraryDir, "tagesthemen.png")
    if (fm.fileExists(path) && !forceDownload) {
        return fm.readImage(path)
    } else {
        const req = new Request("https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Tagesthemen_Logo_2015.svg/320px-Tagesthemen_Logo_2015.svg.png")
        logo = await req.loadImage()
        fm.writeImage(path, logo)
        return logo
    }
}
