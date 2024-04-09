#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTcpSocket>
#include <QProcess>
#include <QMap>
#include <QMessageBox>

#include "addguestform.h"
#include "deleteguestform.h"
#include "findguestbyidform.h"
#include "findguestbyfioform.h"

#include "addroomform.h"
#include "deleteroomform.h"
#include "findroombyidform.h"
#include "findroombyequipmentform.h"

#include "moveinform.h"
#include "departform.h"

QT_BEGIN_NAMESPACE
namespace Ui {
class MainWindow;
}
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

    void sendRequest(const QString &request);
    bool readResponse();

private slots:
    void on_addGuest_clicked();

    void on_addRoom_clicked();

    void on_deleteGuest_clicked();

    void on_findGuestById_clicked();

    void on_findGuestByFio_clicked();

    void on_deleteRoom_clicked();

    void on_findRoomById_clicked();

    void on_findRoomByEquipment_clicked();

    void on_findAllGuests_clicked();

    void on_clearGuests_clicked();

    void on_findAllRooms_clicked();

    void on_clearRooms_clicked();

    void on_moveIn_clicked();

    void on_depart_clicked();

private:
    void closeEvent(QCloseEvent *event);
    void getRegistrations();
    void displayData(QString tabChoice, QString data);
    void closeForm(QString name);
    void clearForm(QString name);
    void clearDisplay();

    Ui::MainWindow *ui;

    addGuestForm *addGuestform;
    DeleteGuestForm *deleteGuestForm;
    FindGuestByIdForm *findGuestByIdForm;
    FindGuestByFioForm *findGuestByFioForm;

    AddRoomForm *addRoomForm;
    DeleteRoomForm *deleteRoomForm;
    FindRoomByIdForm *findRoomByIdForm;
    FindRoomByEquipmentForm *findRoomByEquipmentForm;

    MoveInForm *moveInForm;
    DepartForm * departForm;

    QTcpSocket *socket;
    QMap<QString, QWidget*> formsMap;

    QProcess *pythonProcess;
};
#endif // MAINWINDOW_H
