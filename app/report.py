__author__ = 'brighamhausman'

"""promotes display and commentary of data use it to work with html or pdf rendering libraries, perhaps...
    __section -- one unit of a report containing one visual and commentary
        title - string used for a header for the section
        media - some kind of display besides text
        comments - text to explain and/or emphasize, etc.
    __sections -- ordered list of sections comprising the entire report
    Minimnum report would probably have two sections:
     1. the main intro explaining big
     2. following sections with data visualization and commentary
"""


class Section:
    __title = ''  # header
    __media = ''  # visual or otherwise
    __comments = []

    def __repr__(self):
        showme = 'title: {}\n'.format(self.title)
        showme += 'media: {}\n'.format(self.media)
        showme += 'comments: {}\n'.format(str(self.comments))
        return showme

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def media(self):
        return self.__media

    @media.setter
    def media(self, media):
        self.__media = media

    @property
    def comments(self):
        return self.__comments

    @comments.setter
    def comments(self, comments):
        self.__comments = comments


class Report:
    __sections = []  # list so that you have to change order explicitly
    __title = '' # meta-title that unifies the report sections

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title


    @property
    def sections(self):
        return self.__sections

    def make_section(self, section_data):
        section = Section()
        for key in section_data:
            setattr(section, key, section_data[key])
        self.__sections.append(section)

    def get_section(self, section_index):
        try:
            section = self.__sections[section_index]
        except IndexError:
            section = Section()
            section.title = 'Error'
            section.comments = ['report sections list has no index at: ' + section_index]

        return section

    def update_section(self, section, section_index):
        # TODO: typecheck, please
        self.sections[section_index] = section

    def delete_section(self, section_index):
        self.sections.pop(section_index)


if __name__ == '__main__':
    report = Report()

    section_data = {'title': 'section title', 'media': 'porno.svg', 'comments': [
        'I had something to say...'
    ]}

    # create a section,
    report.make_section(section_data)
    print('########\nstart section')
    print(report.sections)
    # create a second section
    new_section = {}
    new_section['title'] = 'this is the second section'
    new_section['comments'] = ['I have something different to say']
    new_section['media'] = 'porno2.svg'
    report.make_section(new_section)
    # show the list
    print('reports sections')
    print(report.sections)
    # update the first section
    changeme = report.get_section(0)
    changeme.title = 'this is the updated section'
    changeme.comments = ['I say something brand-new now.']
    report.update_section(changeme, 0)
    print('updated reports sections')
    print(report.sections)
    # change the order
    # show the list
    # delete a section
    report.delete_section(1)
    print('deleted reports sections')
    print(report.sections)
