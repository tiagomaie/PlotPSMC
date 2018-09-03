import tkinter
from tkinter import messagebox
from PIL import Image, ImageTk  # PIL is now called pillow for installation purposes
import PlotPSMC
import traceback
from pathlib import Path


class PlotPSMCApp(tkinter.Tk):
    def __init__(self):
        self.psmcOptions = []

        # create a new window
        # tkinter.TopLevel.__init__(self) # might need to use TopLevel if I want to plot on an external window
        tkinter.Tk.__init__(self)

        # self.geometry("665x520")

        # set the window title
        self.title("PlotMyPSMC - Population and Conservation Genetics group")

        # create labels and text entry widgets
        self.descriptionLabel = tkinter.Label(self,
                                              text="PlotMyPSMC allows you to either import a "
                                                   "parameter file (blue) or input your own psmc files, "
                                                   "as well as the necessary options (orange) into this interface, "
                                                   "you always need to specify your plotting options (green).",
                                              wraplength=650, anchor="center", justify="center", bg="gray40")

        # Window bg color
        bgWindowColor = "grey80"

        self.configure(background=bgWindowColor)

        # Make window not-resizable
        self.resizable(0, 0)

        importFromFileColor = "SteelBlue1"; activeImpFromFileCol = "RoyalBlue1"
        importPSMCFileColor = "goldenrod"; activeImpPSMCFileCol = "goldenrod3"
        plottingOptionsColor = "green3"; activePltOptCol = "green4"

        self.default_psmc_opt = {
            "psmcF_path": "",
            "gen_time": "25",
            "mut_rate": "2.5e-8",
            "bin_size": "100",
            "sample_name": "my_sample",
            "sample_color": "red",
        }

        self.default_plt_opt = {
            "xmin": "1e3",
            "xmax": "1e7",
            "ymin": "0",
            "ymax": "1e6",
            "bootstrap_alpha": "0.15",
            "plt_name": "my_PSMC_plot",
        }

        entryBoxWidth = 15

        # widget looks in window
        self.paddingYopt = 2
        self.paddingXopt = 2
        self.stickTo = tkinter.E + tkinter.E

        # widgets row/col positions
        descriptionRow = 0
        pathParFileRow = 1
        buttonPathPar = 2
        pathPSMCFileRow = 3
        generationRow = 4
        mutationRow = 5
        binSizeRow = 6
        sampleNameRow = 7
        lineColorRow = 8

        buttonSaveRow = 9

        xaxisMinRow = 10
        xaxisMaxRow = 11
        yaxisMinRow = 12
        yaxisMaxRow = 13
        bootstrapRow = 14

        savePlotNameRow = 15
        isLogScaleRow = 16
        plotLGMRow = 17
        buttonPlot = plotRowSpan = 18
        logReportRow = 19

        labelColumns = 0
        entryColumns = 1

        self.pathToParFileLabel = tkinter.Label(self, text="Path to parameter file", bg=importFromFileColor)
        self.pathToParFileEntry = tkinter.Entry(self, width=entryBoxWidth)
        self.add_placeholder_to(self.pathToParFileEntry, "")

        self.importFromFileButton = tkinter.Button(
            self, text="Import from parameter file",
            command=self.on_button_import_from_file,
            bg=importFromFileColor,
            activebackground=activeImpFromFileCol
        )

        # set PSMC default opts
        self.pathToPsmcFileLabel = tkinter.Label(self, text="Path to PSMC file", bg=importPSMCFileColor)
        self.pathToPsmcFileEntry = tkinter.Entry(self, width=entryBoxWidth)
        self.add_placeholder_to(self.pathToPsmcFileEntry, self.default_psmc_opt.get("psmcF_path"))

        self.generationTimeLabel = tkinter.Label(self, text="Generation time", bg=importPSMCFileColor)
        self.generationTimeEntry = tkinter.Entry(self, width=entryBoxWidth)
        self.add_placeholder_to(self.generationTimeEntry, self.default_psmc_opt.get("gen_time"))

        self.mutRateLabel = tkinter.Label(self, text="Mutation rate", bg=importPSMCFileColor)
        self.mutRateEntry = tkinter.Entry(self, width=entryBoxWidth)
        self.add_placeholder_to(self.mutRateEntry, self.default_psmc_opt.get("mut_rate"))

        self.binSizeLabel = tkinter.Label(self, text="Bin size", bg=importPSMCFileColor)
        self.binSizeEntry = tkinter.Entry(self, width=entryBoxWidth)
        self.add_placeholder_to(self.binSizeEntry, self.default_psmc_opt.get("bin_size"))

        self.sampleNameLabel = tkinter.Label(self, text="Sample name", bg=importPSMCFileColor)
        self.sampleNameEntry = tkinter.Entry(self, width=entryBoxWidth)
        self.add_placeholder_to(self.sampleNameEntry, self.default_psmc_opt.get("sample_name"))

        self.lineColorLabel = tkinter.Label(self, text="Line color", bg=importPSMCFileColor)
        self.lineColorEntry = tkinter.Entry(self, width=entryBoxWidth)
        self.add_placeholder_to(self.lineColorEntry, self.default_psmc_opt.get("sample_color"))

        # set plot default opts
        self.xminLabel = tkinter.Label(self, text="X axis minimum value", bg=plottingOptionsColor)
        self.xminEntry = tkinter.Entry(self, width=entryBoxWidth)
        self.add_placeholder_to(self.xminEntry, self.default_plt_opt.get("xmin"))

        self.xmaxLabel = tkinter.Label(self, text="X axis maximum value", bg=plottingOptionsColor)
        self.xmaxEntry = tkinter.Entry(self, width=entryBoxWidth)
        self.add_placeholder_to(self.xmaxEntry, self.default_plt_opt.get("xmax"))

        self.yminLabel = tkinter.Label(self, text="Y axis minimum value", bg=plottingOptionsColor)
        self.yminEntry = tkinter.Entry(self, width=entryBoxWidth)
        self.add_placeholder_to(self.yminEntry, self.default_plt_opt.get("ymin"))

        self.ymaxLabel = tkinter.Label(self, text="Y axis maximum value", bg=plottingOptionsColor)
        self.ymaxEntry = tkinter.Entry(self, width=entryBoxWidth)
        self.add_placeholder_to(self.ymaxEntry, self.default_plt_opt.get("ymax"))

        self.transparencyLabel = tkinter.Label(self, text="Bootstrap transparency", bg=plottingOptionsColor)
        self.transparencyEntry = tkinter.Entry(self, width=entryBoxWidth)
        self.add_placeholder_to(self.transparencyEntry, self.default_plt_opt.get("bootstrap_alpha"))

        self.savePlotNameLabel = tkinter.Label(self, text="Plot Name", bg=plottingOptionsColor)
        self.savePlotNameEntry = tkinter.Entry(self, width=entryBoxWidth)
        self.add_placeholder_to(self.savePlotNameEntry, self.default_plt_opt.get("plt_name"))

        self.saveButton = tkinter.Button(
            self, text="Save options",
            command=self.on_button_save,
            bg=importPSMCFileColor,
            activebackground=activeImpPSMCFileCol
        )

        self.clearButton = tkinter.Button(
            self, text="Clear all options",
            command=self.on_button_clear,
            bg=importPSMCFileColor,
            activebackground=activeImpPSMCFileCol
        )
        self.plotButton = tkinter.Button(
            self, text="Plot PSMC",
            command=self.on_button_plot,
            bg=plottingOptionsColor,
            activebackground=activePltOptCol
        )

        self.isLogScaleLabel = tkinter.Label(self, text="Plot in log scale?", bg=plottingOptionsColor)
        self.isXLogScale = tkinter.BooleanVar()
        self.isXLogScaleCheckButton = tkinter.Checkbutton(
            self, variable=self.isXLogScale,
            onvalue=True,
            offvalue=False,
            text="x",
            anchor="c",
            fg="black",
            bg=bgWindowColor,
            justify="center",
            highlightthickness=0,
            activebackground=plottingOptionsColor
        )
        self.isXLogScaleCheckButton.select()

        self.isYLogScale = tkinter.BooleanVar()
        self.isYLogScaleCheckButton = tkinter.Checkbutton(
            self, variable=self.isYLogScale,
            onvalue=True,
            offvalue=False,
            text="y",
            anchor="c",
            fg="black",
            bg=bgWindowColor,
            justify="center",
            highlightthickness=0,
            activebackground=plottingOptionsColor
        )
        self.isYLogScaleCheckButton.deselect()

        self.plotLGMLabel = tkinter.Label(self, text="Plot LGM?", bg=plottingOptionsColor)
        self.doPlotLGM = tkinter.BooleanVar()
        self.plotLGMButton = tkinter.Checkbutton(
            self, variable=self.doPlotLGM,
            onvalue=True,
            offvalue=False,
            anchor="c",
            fg="black",
            bg=bgWindowColor,
            justify="center",
            highlightthickness=0,
            activebackground=plottingOptionsColor
        )
        self.plotLGMButton.select()

        self.logReportString = tkinter.StringVar()
        self.logReportLabel = tkinter.Label(
            self, textvariable=self.logReportString,
            wraplength=950,
            anchor="center",
            justify="center",
            bg="black",
            fg="white"
        )


        # add the widgets into the window
        # description
        self.descriptionLabel.grid(
            row=descriptionRow,
            column=labelColumns,
            columnspan=3,
            pady=self.paddingYopt,
            padx=self.paddingXopt,
            sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W
        )

        # path to parameter file and respective button to import
        self.pathToParFileLabel.grid(
            row=pathParFileRow,
            column=labelColumns,
            pady=self.paddingYopt,
            padx=self.paddingXopt,
            sticky=self.stickTo
        )

        self.pathToParFileEntry.grid(row=pathParFileRow, column=entryColumns)
        self.importFromFileButton.grid(
            row=buttonPathPar,
            column=0,
            columnspan=2,
            pady=self.paddingYopt
        )

        #  path to psmc file
        self.pathToPsmcFileLabel.grid(
            row=pathPSMCFileRow,
            column=labelColumns,
            pady=self.paddingYopt,
            padx=self.paddingXopt,
            sticky=self.stickTo
        )
        self.pathToPsmcFileEntry.grid(row=pathPSMCFileRow, column=entryColumns)

        #  generation time
        self.generationTimeLabel.grid(
            row=generationRow,
            column=labelColumns,
            pady=self.paddingYopt,
            padx=self.paddingXopt,
            sticky=self.stickTo
        )
        self.generationTimeEntry.grid(row=generationRow, column=entryColumns)

        #  mutation rate
        self.mutRateLabel.grid(
            row=mutationRow,
            column=labelColumns,
            pady=self.paddingYopt,
            padx=self.paddingXopt,
            sticky=self.stickTo
        )
        self.mutRateEntry.grid(row=mutationRow, column=entryColumns)

        #  bin size
        self.binSizeLabel.grid(
            row=binSizeRow,
            column=labelColumns,
            pady=self.paddingYopt,
            padx=self.paddingXopt,
            sticky=self.stickTo
        )
        self.binSizeEntry.grid(
            row=binSizeRow,
            column=entryColumns
        )

        #  sample name
        self.sampleNameLabel.grid(
            row=sampleNameRow,
            column=labelColumns,
            pady=self.paddingYopt,
            padx=self.paddingXopt,
            sticky=self.stickTo
        )
        self.sampleNameEntry.grid(
            row=sampleNameRow,
            column=entryColumns
        )

        #  line color
        self.lineColorLabel.grid(
            row=lineColorRow,
            column=labelColumns,
            pady=self.paddingYopt,
            padx=self.paddingXopt,
            sticky=self.stickTo
        )
        self.lineColorEntry.grid(
            row=lineColorRow,
            column=entryColumns
        )

        #  xmin
        self.xminLabel.grid(
            row=xaxisMinRow,
            column=labelColumns,
            pady=self.paddingYopt,
            padx=self.paddingXopt,
            sticky=self.stickTo
        )
        self.xminEntry.grid(
            row=xaxisMinRow,
            column=entryColumns
        )

        #  xmax
        self.xmaxLabel.grid(
            row=xaxisMaxRow,
            column=labelColumns,
            pady=self.paddingYopt,
            padx=self.paddingXopt,
            sticky=self.stickTo
        )
        self.xmaxEntry.grid(
            row=xaxisMaxRow,
            column=entryColumns
        )

        #  ymin
        self.yminLabel.grid(
            row=yaxisMinRow,
            column=labelColumns,
            pady=self.paddingYopt,
            padx=self.paddingXopt,
            sticky=self.stickTo
        )
        self.yminEntry.grid(
            row=yaxisMinRow,
            column=entryColumns
        )

        #  ymax
        self.ymaxLabel.grid(
            row=yaxisMaxRow,
            column=labelColumns,
            pady=self.paddingYopt,
            padx=self.paddingXopt,
            sticky=self.stickTo
        )
        self.ymaxEntry.grid(row=yaxisMaxRow, column=entryColumns)

        #  bootstrap transparency
        self.transparencyLabel.grid(
            row=bootstrapRow,
            column=labelColumns,
            pady=self.paddingYopt,
            padx=self.paddingXopt,
            sticky=self.stickTo
        )
        self.transparencyEntry.grid(row=bootstrapRow, column=entryColumns)

        #  save plot name
        self.savePlotNameLabel.grid(
            row=savePlotNameRow,
            column=labelColumns,
            pady=self.paddingYopt,
            padx=self.paddingXopt,
            sticky=self.stickTo
        )
        self.savePlotNameEntry.grid(row=savePlotNameRow, column=entryColumns)

        #  save button
        self.saveButton.grid(
            row=buttonSaveRow,
            column=0,
            pady=self.paddingYopt,
            padx=self.paddingXopt
        )

        #  clear options button
        self.clearButton.grid(
            row=buttonSaveRow,
            column=1,
            pady=self.paddingYopt,
            padx=self.paddingXopt
        )

        #  plot button
        self.plotButton.grid(
            row=buttonPlot,
            column=0,
            columnspan=2,
            pady=self.paddingYopt
        )

        # is log scale check button
        self.isLogScaleLabel.grid(
            row=isLogScaleRow,
            column=labelColumns,
            pady=self.paddingYopt,
            padx=self.paddingXopt,
            sticky=self.stickTo
        )
        self.isXLogScaleCheckButton.grid(
            row=isLogScaleRow,
            column=entryColumns,
            padx=self.paddingXopt+20,
            pady=self.paddingYopt,
            sticky="w"
        )
        self.isYLogScaleCheckButton.grid(
            row=isLogScaleRow,
            column=entryColumns,
            padx=self.paddingXopt+20,
            pady=self.paddingYopt,
            sticky="e"
        )

        # plot Last Glacial Maximum check button
        self.plotLGMLabel.grid(
            row=plotLGMRow,
            column=labelColumns,
            padx=self.paddingXopt,
            pady=self.paddingYopt,
            sticky=self.stickTo
        )
        self.plotLGMButton.grid(
            row=plotLGMRow,
            column=entryColumns,
            padx=self.paddingXopt,
            pady=self.paddingYopt
        )

        self.logReportLabel.grid(
            row=logReportRow,
            column=labelColumns,
            columnspan=3,
            pady=self.paddingYopt,
            padx=self.paddingXopt,
            sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W
        )

        self.center_window()

        photo = ImageTk.PhotoImage(Image.open("blankPlot.png"))
        self.plotInGrid = tkinter.Label(self, image=photo)
        self.plotInGrid.image = photo
        self.plotInGrid.grid(row=1, column=2, rowspan=plotRowSpan, padx=5, pady=5)

        # on client exit
        self.protocol("WM_DELETE_WINDOW", self.client_exit)
        # client exit with "Escape"
        self.bind('<Escape>', lambda e: self.client_exit())
        # create window variable to hold plot
        self.figWindow = None

        # error reporting
        self.report_callback_exception = self.show_error

    def center_window(self):
        self.eval('tk::PlaceWindow %s center' % self.winfo_pathname(self.winfo_id()))

    def on_button_save(self):
        if Path(self.pathToPsmcFileEntry.get()).is_file():
            self.psmcOptions.append((self.pathToPsmcFileEntry.get(),
                                     float(self.generationTimeEntry.get()),
                                     float(self.mutRateEntry.get()),
                                     float(self.binSizeEntry.get()),
                                     self.sampleNameEntry.get(),
                                     self.lineColorEntry.get()
                                     ))
            self.logReportString.set("Current PSMC entries: \n"+self.psmcOptions.__str__())
        else:
            self.logReportString.set("Please provide a valid path to a PSMC file or import a parameter file.")

    def on_button_plot_externalWindow(self):
        PlotPSMC.plotPsmc(self.psmcOptions, yAsEffectiveSize=True,
                          xmin=float(self.xminEntry.get()),
                          xmax=float(self.xmaxEntry.get()),
                          ymin=float(self.yminEntry.get()),
                          ymax=float(self.ymaxEntry.get()),
                          transparency=float(self.transparencyEntry.get()))

        #  if plot window exists, destroy it
        if self.figWindow:
            self.figWindow.destroy()
        # create plot window
        self.figWindow = tkinter.Toplevel()
        self.figWindow.title("PSMC plot")
        myImage = ImageTk.PhotoImage(Image.open("testPlot.png"))
        imageLabel = tkinter.Label(self.figWindow, image=myImage)
        # imageLabel.pack(side="bottom", fill="both", expand="yes")
        imageLabel.grid(sticky=tkinter.NE + tkinter.SW)

    def on_button_plot(self):
        if self.psmcOptions:
            PlotPSMC.plotPsmc(self.psmcOptions, yAsEffectiveSize=True,
                              xmin=float(self.xminEntry.get()),
                              xmax=float(self.xmaxEntry.get()),
                              ymin=float(self.yminEntry.get()),
                              ymax=float(self.ymaxEntry.get()),
                              transparency=float(self.transparencyEntry.get()),
                              isXLogScale=self.isXLogScale.get(),
                              isYLogScale=self.isYLogScale.get(),
                              showLGM=self.doPlotLGM.get(),
                              savePlotWithName=self.savePlotNameEntry.get())
            myImage = ImageTk.PhotoImage(Image.open("./Plots/" + self.savePlotNameEntry.get() + ".png"))
            self.plotInGrid.configure(image=myImage)
            self.plotInGrid.image = myImage
            self.logReportString.set(
                "Plotted image from the following PSMC entries: \n" + self.psmcOptions.__str__() +
                ".\n" + "Saved plot as " + self.savePlotNameEntry.get() + ".png."
            )
        else:
            self.logReportString.set("There are no PSMC entries available, nothing to plot.")

    def on_button_clear(self):
        self.psmcOptions = []
        self.logReportString.set("All PSMC entries have been cleared.")

        self.pathToPsmcFileEntry.delete(0, "end")
        self.generationTimeEntry.delete(0, "end")
        self.mutRateEntry.delete(0, "end")
        self.binSizeEntry.delete(0, "end")
        self.sampleNameEntry.delete(0, "end")
        self.lineColorEntry.delete(0, "end")
        self.add_placeholder_to(self.pathToPsmcFileEntry, self.default_psmc_opt.get("psmcF_path"))
        self.add_placeholder_to(self.generationTimeEntry, self.default_psmc_opt.get("gen_time"))
        self.add_placeholder_to(self.mutRateEntry, self.default_psmc_opt.get("mut_rate"))
        self.add_placeholder_to(self.binSizeEntry, self.default_psmc_opt.get("bin_size"))
        self.add_placeholder_to(self.sampleNameEntry, self.default_psmc_opt.get("sample_name"))
        self.add_placeholder_to(self.lineColorEntry, self.default_psmc_opt.get("sample_color"))

    def on_button_import_from_file(self):
        self.psmcOptions = PlotPSMC.readPsmcOptions(self.pathToParFileEntry.get())
        self.logReportString.set("Current PSMC entries: \n" + self.psmcOptions.__str__())

    @staticmethod
    def add_placeholder_to(entry, placeholder):

        entry.insert(0, placeholder)
        entry.config(fg='grey', bg="white")

        def on_entry_click(event, this_entry=entry):
            """function that gets called whenever entry is clicked"""
            if this_entry.cget("fg") == 'grey':
                this_entry.delete(0, "end")  # delete all the text in the entry
                this_entry.insert(0, '')  # Insert blank for user input
                this_entry.config(fg='black', bg="white")

        def on_focusout(event, this_entry=entry, placeholder=placeholder):
            if this_entry.get() == '':
                this_entry.insert(0, placeholder)
                this_entry.config(fg='grey', bg="white")

        entry.bind('<FocusIn>', on_entry_click, add="+")
        entry.bind('<FocusOut>', on_focusout, add="+")

    def client_exit(self):
        tmp_log_msg = self.logReportString.get()
        self.logReportString.set("Bye!?")
        if messagebox.askyesno("PlotMyPSMC", "Are you sure you want to exit?"):
            self.quit()
        self.logReportString.set(tmp_log_msg)

    def show_error(self, *args):
        err = traceback.format_exception(*args)
        print(err)
        # Printing the last token of the error stack
        messagebox.showerror("Oops, there was an error!", err[-1].strip())


def main():
    myWindow = PlotPSMCApp()
    # draw the window and start the application
    myWindow.mainloop()


if __name__ == "__main__":
    main()


# myWindow = PlotPSMCApp()
# draw the window and start the application
# myWindow.mainloop()
