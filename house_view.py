

class HouseView(ViewObject):
    def house(self):
        glBegin(GL_QUADS)
        #Floor
        glVertex3f(-1,-1,-1);
        glVertex3f(1,-1,-1);
        glVertex3f(1,-1,1);
        glVertex3f(-1,-1,1);

        #Ceiling
        glVertex3f(-1,1,-1);
        glVertex3f(1,1,-1);
        glVertex3f(1,1,1);
        glVertex3f(-1,1,1);
        #Walls
        glVertex3f(-1,-1,1);
        glVertex3f(1,-1,1);
        glVertex3f(1,1,1);
        glVertex3f(-1,1,1);

        glVertex3f(-1,-1,-1);
        glVertex3f(1,-1,-1);
        glVertex3f(1,1,-1);
        glVertex3f(-1,1,-1);

        glVertex3f(1,1,1);
        glVertex3f(1,-1,1);
        glVertex3f(1,-1,-1);
        glVertex3f(1,1,-1);

        glVertex3f(-1,1,1);
        glVertex3f(-1,-1,1);
        glVertex3f(-1,-1,-1);
        glVertex3f(-1,1,-1);
        glEnd();
        
    def draw(self):
        self.house()
